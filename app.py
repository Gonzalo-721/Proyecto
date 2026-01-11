import os
from flask import Flask, render_template, request, redirect, session, flash, url_for
from sqlalchemy.orm import joinedload
from models import db, Usuario, Cliente, Empleado, Habitacion, Reserva, Servicio, ConsumoServicio, Pago
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from decimal import Decimal

# ---------------------- CONFIG ----------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "super_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ---------------------- DECORADORES ----------------------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return wrapper

# ---------------------- RUTAS ----------------------
@app.route('/')
def home():
    return redirect('/login')

# --------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario and check_password_hash(usuario.contrasena_hash, contrasena):
            session['usuario_id'] = usuario.id_usuario
            # Redirige según tipo de usuario
            if hasattr(usuario, 'cliente') and usuario.cliente:
                return redirect('/dashboard_cliente')
            elif hasattr(usuario, 'empleado') and usuario.empleado:
                return redirect('/dashboard_empleado')
            else:
                flash("Tipo de usuario desconocido", "error")
                return redirect('/login')
        else:
            flash("Correo o contraseña incorrectos", "error")

    return render_template('login.html')

# --------- REGISTRO ----------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        telefono = request.form['telefono']
        tipo_usuario = request.form['tipo_usuario']

        # Evitar correo duplicado
        if Usuario.query.filter_by(correo=correo).first():
            flash("Correo ya registrado", "error")
            return redirect('/registro')

        hash_pw = generate_password_hash(contrasena)
        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            contrasena_hash=hash_pw,
            telefono=telefono
        )

        db.session.add(usuario)
        db.session.commit()

        if tipo_usuario == "cliente":
            cliente = Cliente(id_usuario=usuario.id_usuario, fecha_registro=datetime.now())
            db.session.add(cliente)
        elif tipo_usuario == "empleado":
            empleado = Empleado(id_usuario=usuario.id_usuario, fecha_contratacion=datetime.now(), salario=0, id_rol=1)
            db.session.add(empleado)    

        db.session.commit()
        flash(f"Usuario {tipo_usuario} creado exitosamente!", "success")
        return redirect('/login')

    return render_template('registro.html')

# --------- DASHBOARDS ----------
@app.route('/dashboard_cliente')
@login_required
def dashboard_cliente():
    usuario = Usuario.query.get(session['usuario_id'])
    if not usuario or not usuario.cliente:
        flash("Acceso no autorizado", "error")
        return redirect('/login')

    cliente = usuario.cliente

    reservas = Reserva.query.options(
        joinedload(Reserva.cliente).joinedload(Cliente.usuario),
        joinedload(Reserva.habitacion),
        joinedload(Reserva.consumos).joinedload(ConsumoServicio.servicio)
    ).filter_by(id_cliente=cliente.id_usuario, estado='Activa')\
        .order_by(Reserva.fecha_inicio.desc()).all()

    detalles_reservas = []

    for reserva in reservas:
        total_consumos = sum(c.subtotal for c in reserva.consumos)
        precio_habitacion = reserva.habitacion.precio_noche if reserva.habitacion else 0

        detalles_reservas.append({
            "reserva": reserva,
            "consumos": reserva.consumos,
            "total": total_consumos + precio_habitacion
        })

    return render_template(
        'dashboard_cliente.html',
        usuario=usuario,
        reservas=reservas
    )

@app.route('/dashboard_empleado')
@login_required
def dashboard_empleado():
    usuario = Usuario.query.get(session['usuario_id'])
    if not usuario or not hasattr(usuario, 'empleado') or not usuario.empleado:
        flash("Acceso no autorizado", "error")
        return redirect('/login')

    reservas = Reserva.query.filter_by(estado='Activa').all()
    return render_template('dashboard_empleado.html', usuario=usuario, reservas=reservas)

# --------- GESTIONAR HABITACIONES ---------
@app.route('/gestionar_habitaciones', methods=['GET', 'POST'])
@login_required
def gestionar_habitaciones():
    usuario = Usuario.query.get(session['usuario_id'])
    if not hasattr(usuario, 'empleado'):
        return "Acceso denegado"

    if request.method == 'POST':
        numero = request.form['numero']
        tipo = request.form['tipo']
        precio = request.form['precio_noche']
        habitacion = Habitacion(numero=numero, tipo=tipo, precio_noche=precio, estado='Disponible')
        db.session.add(habitacion)
        db.session.commit()
        return redirect('/gestionar_habitaciones')

    habitaciones = Habitacion.query.order_by(Habitacion.numero).all()
    return render_template('gestionar_habitaciones.html', habitaciones=habitaciones)

# --------- RESERVAS ----------
@app.route('/reservar', methods=['GET', 'POST'])
@login_required
def reservar():
    habitaciones = Habitacion.query.filter_by(estado='Disponible').all()

    if request.method == 'POST':
        fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d')
        fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d')
        id_habitacion = int(request.form['id_habitacion'])

        cliente = Cliente.query.filter_by(id_usuario=session['usuario_id']).first()

        reserva = Reserva(
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin,
            estado='Activa', 
            id_cliente=cliente.id_usuario,
            id_habitacion=id_habitacion
        )

        habitacion = Habitacion.query.get(id_habitacion)
        habitacion.estado = 'Ocupada'

        db.session.add(reserva)
        db.session.commit()

        return redirect('/servicios')

    return render_template('reservar.html', habitaciones=habitaciones)

#--------- VER DETALLES DE LAS RESERVAS (PARA CLIENTES) ---------
@app.route('/detalles_reserva/<int:id_reserva>')
@login_required
def detalles_reserva(id_reserva):
    usuario = Usuario.query.get(session['usuario_id'])
    if not usuario or not usuario.cliente:
        flash("Acceso no autorizado")
        return redirect('/login')

    reserva = Reserva.query.options(
        joinedload(Reserva.habitacion),
        joinedload(Reserva.consumos).joinedload(ConsumoServicio.servicio)
    ).get(id_reserva)

    if not reserva or reserva.id_cliente != usuario.cliente.id_usuario:
        flash("Reserva no encontrada", "error")
        return redirect('/dashboard_cliente')

    total_consumos = sum(c.subtotal for c in reserva.consumos)
    precio_habitacion = reserva.habitacion.precio_noche
    total = total_consumos + precio_habitacion

    return render_template(
        'detalles_reserva.html',
        reserva=reserva,
        total=total
    )

#--------- PAGAR LA RESERVA ---------
@app.route('/pago_reserva/<int:id_reserva>')
@login_required
def pago_reserva(id_reserva):
    usuario = Usuario.query.get(session['usuario_id'])
    if not usuario or not usuario.cliente:
        flash("Acceso no autorizado", "error")
        return redirect('/login')

    reserva = Reserva.query.options(
        joinedload(Reserva.habitacion),
        joinedload(Reserva.consumos).joinedload(ConsumoServicio.servicio)
    ).get(id_reserva)

    if not reserva or reserva.id_cliente != usuario.cliente.id_usuario:
        flash("Reserva no encontrada", "error")
        return redirect('/dashboard_cliente')

    total_consumos = sum(c.subtotal for c in reserva.consumos)
    total = total_consumos + reserva.habitacion.precio_noche 

    return render_template(
        'pago_reserva.html',
        reserva=reserva,
        total=total
    )

#--------- VER RESERVAS ---------
@app.route('/ver_reservas')
@login_required
def ver_reservas():
    usuario = Usuario.query.get(session['usuario_id'])
    if not hasattr(usuario, 'empleado'):
        return "Acceso denegado"

    reservas = Reserva.query.order_by(Reserva.estado.desc(), Reserva.fecha_inicio.desc()).all()
    return render_template('ver_reservas.html', reservas=reservas)

# --------- SERVICIOS ----------
@app.route('/servicios', methods=['GET', 'POST'])
@login_required
def servicios():
    usuario = Usuario.query.get(session['usuario_id'])

    if not hasattr(usuario, 'cliente') or not usuario.cliente:
        flash("Solo clientes pueden agregar servicios", "error")
        return redirect('/login')

    cliente = usuario.cliente
    servicios = Servicio.query.all()

    reserva = Reserva.query.filter_by(
        id_cliente=cliente.id_usuario,
        estado='Activa'
    ).order_by(Reserva.id_reserva.desc()).first()

    if not reserva:
        flash("No tienes una reserva activa", "warning")
        return redirect('/dashboard_cliente')

    if request.method == 'POST':
        id_servicio = request.form.get('id_servicio')

        if not id_servicio or id_servicio == "0":
            flash("No se agregó ningún servicio", "warning")
            return redirect('/dashboard_cliente')

        cantidad = request.form.get('cantidad')

        if not cantidad or int(cantidad) <= 0:
            flash("Cantidad inválida", "error")
            return redirect('/servicios')

        id_servicio = int(id_servicio)
        cantidad = int(cantidad)

        servicio = Servicio.query.get(id_servicio)

        if not servicio:
            flash("Servicio no válido", "error")
            return redirect('/servicios')

        subtotal = servicio.precio * cantidad

        consumo = ConsumoServicio(
            id_reserva=reserva.id_reserva,
            id_servicio=id_servicio,
            cantidad=cantidad,
            subtotal=subtotal
        )

        db.session.add(consumo)
        db.session.commit()

        flash("Servicio agregado correctamente", "success")
        return redirect('/dashboard_cliente')

    return render_template('servicios.html', servicios=servicios)

# --------- ELIMINAR SERVICIOS ---------
@app.route('/eliminar_servicio/<int:id_consumo>', methods=['POST'])
@login_required
def eliminar_servicio(id_consumo):
    usuario = Usuario.query.get(session['usuario_id'])

    consumo = ConsumoServicio.query.get_or_404(id_consumo)
    reserva = Reserva.query.get(consumo.id_reserva)

    if not usuario or not usuario.cliente or reserva.id_cliente != usuario.cliente.id_usuario:
        flash("Acceso no autorizado", "error")
        return redirect('/login')

    db.session.delete(consumo)
    db.session.commit()
    flash("Servicio eliminado correctamente", "success")
    
    return redirect(url_for('editar_servicios', id_reserva=reserva.id_reserva))

# --------- AÑADIR SERVICIOS ---------
@app.route('/agregar_servicio/<int:id_reserva>', methods=['POST'])
@login_required
def agregar_servicio(id_reserva):
    reserva = Reserva.query.get_or_404(id_reserva)

    id_servicio = request.form.get('id_servicio')
    cantidad = request.form.get('cantidad')

    if not id_servicio or not cantidad:
        flash("Selecciona servicio y cantidad", "warning")
        return redirect(url_for('editar_servicios', id_reserva=id_reserva))

    servicio = Servicio.query.get(id_servicio)
    subtotal = servicio.precio * int(cantidad)

    consumo = ConsumoServicio(
        id_reserva=id_reserva,
        id_servicio=id_servicio,
        cantidad=cantidad,
        subtotal=subtotal
    )

    db.session.add(consumo)
    db.session.commit()

    flash("Servicio agregado", "success")
    return redirect(url_for('editar_servicios', id_reserva=id_reserva))

# --------- EDITAR SERVICIOS ---------
@app.route('/editar_servicios/<int:id_reserva>', methods=['GET', 'POST'])
@login_required
def editar_servicios(id_reserva):
    usuario = Usuario.query.get(session['usuario_id'])
    if not usuario or not usuario.cliente:
        flash("Acceso no autorizado", "error")
        return redirect('/login')

    reserva = Reserva.query.options(
        joinedload(Reserva.consumos).joinedload(ConsumoServicio.servicio)
    ).get_or_404(id_reserva)

    if reserva.id_cliente != usuario.cliente.id_usuario:
        flash("No puedes editar esta reserva", "error")
        return redirect(url_for('dashboard_cliente'))

    servicios = Servicio.query.all()

    if 'consumos_temporales' not in session:
        session['consumos_temporales'] = []

    if 'consumos_eliminar' not in session:
        session['consumos_eliminar'] = []

    if request.method == 'POST':
        accion = request.form.get('accion')

        if accion and accion.startswith("eliminar_"):
            id_consumo = int(accion.split("_")[1])
            if id_consumo not in session['consumos_eliminar']:
                session['consumos_eliminar'].append(id_consumo)
                session.modified = True
                flash("Servicio marcado para eliminar", "warning")
            return redirect(url_for('editar_servicios', id_reserva=id_reserva))

        elif accion == "añadir":
            id_servicio_nuevo = request.form.get('id_servicio_nuevo')
            cantidad_nuevo = request.form.get('cantidad_nuevo')

            if not id_servicio_nuevo or not cantidad_nuevo or int(cantidad_nuevo) <= 0:
                flash("Selecciona un servicio válido y cantidad mayor a 0", "warning")
            else:
                servicio = Servicio.query.get(int(id_servicio_nuevo))
                cantidad_nuevo = int(cantidad_nuevo)
                subtotal = float(servicio.precio) * cantidad_nuevo

                found = False
                for temp in session['consumos_temporales']:
                    if temp['id_servicio'] == servicio.id_servicio:
                        temp['cantidad'] += cantidad_nuevo
                        temp['subtotal'] += subtotal
                        found = True
                        break

                if not found:
                    session['consumos_temporales'].append({
                        'id_servicio': servicio.id_servicio,
                        'nombre': servicio.nombre,
                        'cantidad': cantidad_nuevo,
                        'subtotal': subtotal
                    })

                session.modified = True
                flash(f"Servicio '{servicio.nombre}' agregado temporalmente: ${subtotal:.2f}", "success")

            return redirect(url_for('editar_servicios', id_reserva=id_reserva))

        elif accion == "confirmar":
            # 1️⃣ Eliminar servicios marcados
            for id_c in session.get('consumos_eliminar', []):
                consumo = ConsumoServicio.query.get(id_c)
                if consumo:
                    db.session.delete(consumo)

            session.pop('consumos_eliminar', None)

            # 2️⃣ Actualizar cantidades existentes
            ids = request.form.getlist('id_servicio[]')
            cantidades = request.form.getlist('cantidad[]')

            for id_s, cant in zip(ids, cantidades):
                if not id_s or int(cant) <= 0:
                    continue
                id_s = int(id_s)
                cant = int(cant)
                consumo = ConsumoServicio.query.filter_by(
                    id_reserva=id_reserva,
                    id_servicio=id_s
                ).first()
                if consumo:
                    servicio = Servicio.query.get(id_s)
                    consumo.cantidad = cant
                    consumo.subtotal = float(servicio.precio) * cant

            for temp in session.get('consumos_temporales', []):
                temp_cantidad = int(temp['cantidad'])
                temp_subtotal = float(temp['subtotal'])
                consumo = ConsumoServicio.query.filter_by(
                    id_reserva=id_reserva,
                    id_servicio=temp['id_servicio']
                ).first()
                if consumo:
                    consumo.cantidad += temp_cantidad
                    consumo.subtotal += temp_subtotal
                else:
                    consumo = ConsumoServicio(
                        id_reserva=id_reserva,
                        id_servicio=temp['id_servicio'],
                        cantidad=temp_cantidad,
                        subtotal=temp_subtotal
                    )
                    db.session.add(consumo)

            db.session.commit()
            session.pop('consumos_temporales', None)
            flash("Cambios confirmados", "success")
            return redirect(url_for('detalles_reserva', id_reserva=id_reserva))

        elif accion == "cancelar":
            session.pop('consumos_temporales', None)
            session.pop('consumos_eliminar', None)
            flash("Cambios cancelados", "warning")
            return redirect(url_for('detalles_reserva', id_reserva=id_reserva))

    consumos = list(reserva.consumos)
    consumos_temporales = session.get('consumos_temporales', [])
    consumos_eliminar = session.get('consumos_eliminar', [])

    tabla_combinada = {}

    for c in consumos:
        tabla_combinada[c.id_servicio] = {
            'id_servicio': c.id_servicio,
            'id_consumo': c.id_consumo,
            'nombre': c.servicio.nombre,
            'cantidad': int(c.cantidad),
            'subtotal': float(c.subtotal),
            'marcado_eliminar': c.id_consumo in consumos_eliminar
        }

    for t in consumos_temporales:
        if t['id_servicio'] in tabla_combinada:
            tabla_combinada[t['id_servicio']]['cantidad'] += int(t['cantidad'])
            tabla_combinada[t['id_servicio']]['subtotal'] += float(t['subtotal'])
        else:
            tabla_combinada[t['id_servicio']] = {
                'id_servicio': t['id_servicio'],
                'id_consumo': None,
                'nombre': t['nombre'],
                'cantidad': int(t['cantidad']),
                'subtotal': float(t['subtotal']),
                'marcado_eliminar': False
            }

    consumos_para_tabla = list(tabla_combinada.values())

    return render_template(
        'editar_servicios.html',
        reserva=reserva,
        servicios=servicios,
        consumos_temporales=consumos_temporales,
        consumos=consumos_para_tabla
    )

# --------- GESTIONAR SERVICIOS ---------
@app.route('/gestionar_servicios', methods=['GET', 'POST'])
@login_required
def gestionar_servicios():
    usuario = Usuario.query.get(session['usuario_id'])
    if not hasattr(usuario, 'empleado'):
        return "Acceso denegado"

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        servicio = Servicio(nombre=nombre, precio=precio)
        db.session.add(servicio)
        db.session.commit()
        return redirect('/gestionar_servicios')

    servicios = Servicio.query.order_by(Servicio.nombre).all()
    return render_template('gestionar_servicios.html', servicios=servicios)

# --------- CERRAR RESERVA ---------
@app.route('/cerrar_reserva/<int:id_reserva>', methods=['POST'])
@login_required
def cerrar_reserva(id_reserva):
    usuario = Usuario.query.get(session['usuario_id'])
    if not usuario or not usuario.cliente:
        flash("Solo clientes pueden cerrar reservas", "warning")
        return redirect('/login')

    reserva = Reserva.query.get(id_reserva)
    if not reserva or reserva.id_cliente != usuario.cliente.id_usuario:
        flash("Reserva no encontrada", "error")
        return redirect('/dashboard_cliente')

    reserva.estado = 'Finalizada'
    reserva.habitacion.estado = 'Disponible'

    db.session.commit()

    flash("Reserva pagada correctamente", "success")
    return redirect('/dashboard_cliente')

#--------- CANCELAR RESERVA ---------
@app.route('/cancelar_reserva/<int:id_reserva>', methods=['POST'])
@login_required
def cancelar_reserva(id_reserva):
    usuario = Usuario.query.get(session['usuario_id'])
    if not usuario or not usuario.cliente:
        flash("Acción no autorizada", "error")
        return redirect('/login')

    reserva = Reserva.query.get_or_404(id_reserva)

    if reserva.id_cliente != usuario.cliente.id_usuario:
        flash("No puedes cancelar esta reserva", "error")
        return redirect('/dashboard_cliente')

    reserva.estado = 'Cancelada'
    reserva.habitacion.estado = 'Disponible'

    db.session.commit()
    flash("Reserva cancelada correctamente", "success")

    return redirect('/dashboard_cliente')

# --------- CONFIRMAR CANCELACIÓN ---------
@app.route('/confirmar_cancelacion/<int:id_reserva>')
@login_required
def confirmar_cancelacion(id_reserva):
    usuario = Usuario.query.get(session['usuario_id'])
    if not usuario or not usuario.cliente:
        flash("Acceso no autorizado", "error")
        return redirect('/login')

    reserva = Reserva.query.options(
        joinedload(Reserva.habitacion),
        joinedload(Reserva.consumos).joinedload(ConsumoServicio.servicio)
    ).get(id_reserva)

    if not reserva or reserva.id_cliente != usuario.cliente.id_usuario:
        flash("Reserva no encontrada", "error")
        return redirect('/dashboard_cliente')

    total_consumos = sum(c.subtotal for c in reserva.consumos)
    total = total_consumos + reserva.habitacion.precio_noche

    return render_template('cancelar_reserva.html',
        reserva=reserva,
        total=total
    )

# --------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada", "warning")
    return redirect('/login')

# ---------------------- RUN ----------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)






















