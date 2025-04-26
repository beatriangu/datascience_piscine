# Makefile para gestionar servicios con Docker Compose

# Archivo de configuración de Docker Compose
docker_compose_file := docker-compose.yml

# Variables de entorno (ajusta según tu entorno)
export POSTGRES_USER := bea
export POSTGRES_PASSWORD := mysecretpassword
export POSTGRES_DB := piscineds

# --- Levantar todos los servicios (db, app, pgadmin) ---
.PHONY: up
up:
	@echo "🚀 Levantando todos los servicios con Docker Compose"
	docker-compose -f $(docker_compose_file) up -d

# --- Detener todos los servicios (sin eliminar volúmenes) ---
.PHONY: down
down:
	@echo "🛑 Deteniendo todos los servicios"
	docker-compose -f $(docker_compose_file) stop

# --- Limpiar contenedores, redes y volúmenes ---
.PHONY: clean
clean:
	@echo "🧹 Limpiando contenedores, redes y volúmenes"
	docker-compose -f $(docker_compose_file) down -v --remove-orphans

# --- Reiniciar todos los servicios ---
.PHONY: restart
restart: clean up
	@echo "🔄 Reiniciando todos los servicios"

# --- Levantar solo pgAdmin ---
.PHONY: pgadmin
pgadmin:
	@echo "🚀 Levantando solo pgAdmin"
	docker-compose -f $(docker_compose_file) up -d pgadmin

# --- Detener pgAdmin ---
.PHONY: pgadmin-stop
pgadmin-stop:
	@echo "🛑 Deteniendo pgAdmin"
	docker-compose -f $(docker_compose_file) stop pgadmin

# --- Levantar solo la base de datos ---
.PHONY: db
db:
	@echo "🚀 Levantando solo la base de datos"
	docker-compose -f $(docker_compose_file) up -d db

# --- Detener la base de datos ---
.PHONY: db-stop
db-stop:
	@echo "🛑 Deteniendo la base de datos"
	docker-compose -f $(docker_compose_file) stop db

# --- Acceder al shell del contenedor de la aplicación ---
.PHONY: shell
shell:
	@echo "🔗 Abriendo shell en contenedor 'app'"
	docker-compose -f $(docker_compose_file) exec app bash

# --- Mostrar logs de todos los servicios ---
.PHONY: logs
logs:
	@echo "📋 Mostrando logs de todos los servicios"
	docker-compose -f $(docker_compose_file) logs -f

# --- Abrir pgAdmin 4 GUI nativa (macOS) ---
.PHONY: pgadmin-native
pgadmin-native:
	@echo "🔗 Abriendo pgAdmin 4 GUI nativa (macOS)"
	open -a "pgAdmin 4"
