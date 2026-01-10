from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuario"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))

    cliente = db.relationship("Cliente", back_populates="usuario", uselist=False)
    empleado = db.relationship("Empleado", back_populates="usuario", uselist=False)


class RolEmpleado(db.Model):
    __tablename__ = "rol_empleado"

    id_rol = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(50), unique=True, nullable=False)

    empleados = db.relationship("Empleado", back_populates="rol")


class Cliente(db.Model):
    __tablename__ = "cliente"

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id_usuario", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    fecha_registro = db.Column(db.Date, nullable=False)
    tipo_cliente = db.Column(db.String(30))

    usuario = db.relationship("Usuario", back_populates="cliente")
    reservas = db.relationship("Reserva", back_populates="cliente")


class Empleado(db.Model):
    __tablename__ = "empleado"

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id_usuario", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    fecha_contratacion = db.Column(db.Date, nullable=False)
    salario = db.Column(db.Numeric(10, 2))
    id_rol = db.Column(
        db.Integer,
        db.ForeignKey("rol_empleado.id_rol", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    usuario = db.relationship("Usuario", back_populates="empleado")
    rol = db.relationship("RolEmpleado", back_populates="empleados")


class Habitacion(db.Model):
    __tablename__ = "habitacion"

    id_habitacion = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    precio_noche = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.String(30), nullable=False)

    reservas = db.relationship("Reserva", back_populates="habitacion")


class Reserva(db.Model):
    __tablename__ = "reserva"

    id_reserva = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(30), nullable=False)

    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey("cliente.id_usuario", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )
    id_habitacion = db.Column(
        db.Integer,
        db.ForeignKey("habitacion.id_habitacion", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    cliente = db.relationship("Cliente", back_populates="reservas")
    habitacion = db.relationship("Habitacion", back_populates="reservas")
    pagos = db.relationship("Pago", back_populates="reserva")
    consumos = db.relationship("ConsumoServicio", back_populates="reserva")


class Servicio(db.Model):
    __tablename__ = "servicio"

    id_servicio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)

    consumos = db.relationship("ConsumoServicio", back_populates="servicio")


class Pago(db.Model):
    __tablename__ = "pago"

    id_pago = db.Column(db.Integer, primary_key=True)
    fecha_pago = db.Column(db.Date, nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    metodo_pago = db.Column(db.String(50))
    estado_pago = db.Column(db.String(30))

    id_reserva = db.Column(
        db.Integer,
        db.ForeignKey("reserva.id_reserva", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )

    reserva = db.relationship("Reserva", back_populates="pagos")


class ConsumoServicio(db.Model):
    __tablename__ = "consumo_servicio"

    id_consumo = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    id_reserva = db.Column(
        db.Integer,
        db.ForeignKey("reserva.id_reserva", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    id_servicio = db.Column(
        db.Integer,
        db.ForeignKey("servicio.id_servicio", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    reserva = db.relationship("Reserva", back_populates="consumos")
    servicio = db.relationship("Servicio", back_populates="consumos")
