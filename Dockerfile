# Utiliza Python 3.8 Alpine como imagen base
ARG PYTHON_VERSION=python:3.12.3-alpine
FROM ${PYTHON_VERSION}

RUN apk add --no-cache build-base

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Copia el script de entrada al contenedor
COPY entrypoint.sh /app/entrypoint.sh

# Asegura que el script tenga permisos de ejecución
RUN chmod +x /app/entrypoint.sh

EXPOSE 8080

# Configura el entrypoint para ejecutar las migraciones y levantar el servidor
ENTRYPOINT ["/app/entrypoint.sh"]
