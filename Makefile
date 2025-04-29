# Makefile para gestionar servicios con Docker Compose

# Archivo de configuración de Docker Compose
docker_compose_file := docker-compose.yml

# Variables de entorno
export POSTGRES_USER := bea
export POSTGRES_PASSWORD := mysecretpassword
export POSTGRES_DB := piscineds

# --- Levantar todos los servicios (db, app, pgadmin) ---
.PHONY: up
up:
	@echo "🚀 Levantando todos los servicios con Docker Compose"
	docker-compose -f $(docker_compose_file) up -d

# --- Detener todos los servicios ---
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

# --- Acceder a la terminal de PostgreSQL ---
.PHONY: db-shell
db-shell:
	@echo "🛢️  Conectando a PostgreSQL"
	docker-compose -f $(docker_compose_file) exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

# --- Ejecutar script SQL ---
.PHONY: run-sql
run-sql:
	@echo "📜 Ejecutando script SQL"
	docker-compose -f $(docker_compose_file) exec -T db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "$(shell cat fusion.sql)"

# --- Levantar solo pgAdmin ---
.PHONY: pgadmin
pgadmin:
	@echo "📊 Levantando pgAdmin"
	docker-compose -f $(docker_compose_file) up -d pgadmin

# --- Acceder al shell de la aplicación ---
.PHONY: shell
shell:
	@echo "🐚 Abriendo shell en contenedor 'app'"
	docker-compose -f $(docker_compose_file) exec app sh

# --- Ejecutar análisis Mustache ---
.PHONY: mustache
mustache:
	@echo "📊 Generando gráficos Mustache"
	docker-compose -f $(docker_compose_file) exec app python mustache.py

# --- Mostrar logs ---
.PHONY: logs
logs:
	@echo "📋 Mostrando logs"
	docker-compose -f $(docker_compose_file) logs -f

# --- Verificar estado de la DB ---
.PHONY: check-db
check-db:
	@echo "🔍 Verificando estado de PostgreSQL"
	docker-compose -f $(docker_compose_file) exec db pg_isready