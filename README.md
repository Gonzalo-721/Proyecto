
# Sistema de Gestión de Reservas de un Hotel

---

## Resumen

Sistema web integral para la gestión de reservas de hotel, administración de habitaciones y solicitud de servicios adicionales. La plataforma permite a los clientes registrarse, buscar habitaciones disponibles, realizar reservas y gestionar sus consumos de servicios. Para los empleados, ofrece herramientas para visualizar y gestionar reservas activas, habitaciones y servicios ofrecidos

Construida como una aplicación monolítica en Flask con SQLAlchemy (PostgreSQL) y frontend basado en plantillas Jinja2, CSS y JavaScript para una experiencia de usuario fluida (con soporte de modo oscuro)

---

## Contenido

- Resumen
- Modelo relacional
- Arquitectura
- Componentes principales
- Lenguajes y tecnologías
- Despliegue
- Estructura del proyecto
- Base de datos y Modelos
- Seguridad y buenas prácticas
- Logs y monitoreo

---
## Modelo relacional
<img alt="Modelo relacional" src="images/modelo_relacional.png" />

## Arquitectura

- **Frontend**: Plantillas `Jinja2` renderizadas en el servidor + CSS nativo para estilos (modo claro/oscuro) + JavaScript vanilla para interacciones dinámicas
- **Backend**: `Flask` manejando rutas, autenticación y lógica de negocio en `app.py`

### Frontend
- **Motor de Plantillas**: `Jinja2` renderiza el HTML dinámicamente en el servidor, permitiendo herencia de plantillas y paso de datos eficiente desde el backend
- **Estilos**: CSS nativo y modular. Cada vista cuenta con su propia hoja de estilos (ej. `login.css`, `dashboard_cliente.css`) para mantener un código limpio y evitar conflictos de especificidad. Soporta cambio de tema (claro/oscuro)
- **Interactividad**: JavaScript Vanilla ligero para validaciones en cliente y mejoras de UX

### Backend
- **Core**: Construido en `Flask`, el archivo `app.py` centraliza la lógica de control, manejando el enrutamiento, autenticación y orquestación de servicios
- **ORM**: `SQLAlchemy` abstrae la capa de datos, permitiendo interactuar con PostgreSQL mediante objetos Python (`models.py`) en lugar de SQL crudo
- **Seguridad**: Implementación robusta de hashing de contraseñas con `Werkzeug` y manejo seguro de sesiones de usuario


---

## Componentes principales

- `app.py`: Controlador principal. Define las rutas, lógica de autenticación (Login/Registro), dashboards (Cliente/Empleado) y gestión de reservas
- `models.py`: Definición de modelos ORM (`Usuario`, `Cliente`, `Empleado`, `Habitacion`, `Reserva`, `Servicio`, etc.)
- `templates/`: Archivos HTML con Jinja2. Incluye vistas para login, dashboards, gestión de servicios y detalles de reserva
- `static/`: Contiene archivos CSS (estilos específicos para cada vista) e imágenes (`img/`)
- `Procfile`: Archivo de configuración para despliegue en plataformas como Render

---

## Lenguajes y tecnologías

- **Python 3.10+**
- **PostgreSQL**
- Dependencias de Python listadas en `requirements.txt`:
  - Flask
  - Flask-SQLAlchemy
  - psycopg2-binary
  - Werkzeug
  - gunicorn

## Despliegue (Render)

El proyecto está optimizado para su despliegue en **Render** como Web Service:

1. **Crear nuevo Web Service** en Render conectado a este repositorio
2. **Configuración de Build**:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
3. **Variables de Entorno**:
   - `DATABASE_URL`: String de conexión (Render proporciona una base de datos PostgreSQL interna)
   - `SECRET_KEY`: Clave aleatoria segura para sesiones

El archivo `Procfile` incluido facilita la detección automática del comando de inicio

---

## Estructura del proyecto

```text
PROYECTO/
├─ app.py                      # Controlador principal (Rutas y Lógica)
├─ models.py                   # Modelos de Base de Datos (SQLAlchemy)
├─ requirements.txt            # Dependencias Python
├─ Dockerfile                  # Imagen Docker
├─ docker-compose.yml          # Orquestación de servicios
├─ Procfile                    # Comando de inicio
├─ proyectobases.sql           # Script SQL de referencia
├─ static/
│  ├─ css/                     # Estética de la página
│  │  ├─ cancelar_reserva.css
│  │  ├─ dashboard_cliente.css
│  │  ├─ dashboard_empleado.css
│  │  ├─ detalles_reserva.css
│  │  ├─ editar_servicios.css
│  │  ├─ gestionar_habitaciones.css
│  │  ├─ gestionar_servicios.css
│  │  ├─ login.css
│  │  ├─ pago_reserva.css
│  │  ├─ registro.css
│  │  ├─ reservar.css
│  │  ├─ servicios.css
│  │  ├─ ver_reservas.css
│  │  └─ ver_reservas_empleados.css
│  └─ img/
│     └─ logo.png
└─ templates/                  # Vistas HTML (Jinja2)
   ├─ cancelar_reserva.html
   ├─ dashboard_cliente.html
   ├─ dashboard_empleado.html
   ├─ detalles_reserva.html
   ├─ editar_servicios.html
   ├─ gestionar_habitaciones.html
   ├─ gestionar_servicios.html
   ├─ login.html
   ├─ pago_reserva.html
   ├─ registro.html
   ├─ reservar.html
   ├─ servicios.html
   ├─ ver_reservas.html
   └─ ver_reservas_empleados.html
```

<table width="100%" cellspacing="15" cellpadding="0" style="border-collapse: separate;">

  <tr>
    <td width="50%"><img src="images/dashboard_cliente.png" alt="Interfaz usuario 1" width="100%"></td>
    <td width="50%"><img src="images/cancelar_reserva.png" alt="Interfaz usuario 2" width="100%"></td>
  </tr>
  <tr>
    <td width="50%"><img src="images/dashboard_empleado.png" alt="Interfaz usuario 3" width="100%"></td>
    <td width="50%"><img src="images/ver_reservas.png" alt="Interfaz usuario 4" width="100%"></td>
  </tr>
</table>

---

## Base de datos y Modelos

El sistema utiliza un esquema relacional definido en `models.py`. Las principales entidades son:

- **Usuario**: Tabla base para autenticación (correo, contraseña hasheada)
- **RolEmpleado**: Roles para diferenciar permisos de empleados
- **Cliente**: Extensión de Usuario, maneja información específica de clientes
- **Empleado**: Extensión de Usuario, vinculado a un Rol y salario
- **Habitacion**: Inventario de habitaciones (Número, Tipo, Precio, Estado)
- **Reserva**: Núcleo del sistema. Vincula Cliente y Habitación con fechas y Estado
- **Servicio**: Catálogo de servicios adicionales (ej. Restaurante, Spa)
- **ConsumoServicio**: Tabla pivote para registrar servicios consumidos en una Reserva
- **Pago**: Registro de transacciones asociadas a una Reserva

---

## Seguridad y buenas prácticas

- **Autenticación**: Uso de `werkzeug.security` para hashear contraseñas (`generate_password_hash`, `check_password_hash`)
- **Control de Acceso**: Decorador `@login_required` para proteger rutas sensibles. Verificación de roles (Cliente vs Empleado) en cada controlador
- **Sesiones**: Gestión segura de sesiones mediante `Flask-Session` (o cookies firmadas por `SECRET_KEY`)
- **Validación**: Comprobaciones de stock/disponibilidad antes de confirmar reservas

---

## Logs y monitoreo

- La aplicación utiliza `flash` messages para feedback al usuario (errores, confirmaciones)

---

