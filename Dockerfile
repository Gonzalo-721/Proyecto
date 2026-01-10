# Dockerfile para Postgres 17

FROM postgres:17

# Puedes agregar configuraciones adicionales aquí si lo necesitas
# Por ejemplo, copiar archivos de configuración personalizados:
# COPY ./postgresql.conf /etc/postgresql/postgresql.conf

# Exponer el puerto por defecto
EXPOSE 5432

# El contenedor se inicia con el comando por defecto de la imagen oficial