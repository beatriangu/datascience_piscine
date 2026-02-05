# Makefile to manage services with Docker Compose

# Docker Compose configuration file
docker_compose_file := docker-compose.yml

# Environment variables
export POSTGRES_USER := bea
export POSTGRES_PASSWORD := mysecretpassword
export POSTGRES_DB := piscineds

# --- Start all services (db, app, pgadmin) ---
.PHONY: up
up:
	@echo "🚀 Starting all services with Docker Compose"
	docker-compose -f $(docker_compose_file) up -d

# --- Stop all services ---
.PHONY: down
down:
	@echo "🛑 Stopping all services"
	docker-compose -f $(docker_compose_file) stop

# --- Remove containers, networks, and volumes ---
.PHONY: clean
clean:
	@echo "🧹 Cleaning containers, networks, and volumes"
	docker-compose -f $(docker_compose_file) down -v --remove-orphans

# --- Restart all services ---
.PHONY: restart
restart: clean up
	@echo "🔄 Restarting all services"

# --- Open PostgreSQL shell ---
.PHONY: db-shell
db-shell:
	@echo "🛢️  Connecting to PostgreSQL"
	docker-compose -f $(docker_compose_file) exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

# --- Execute SQL script ---
.PHONY: run-sql
run-sql:
	@echo "📜 Executing SQL script"
	docker-compose -f $(docker_compose_file) exec -T db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "$(shell cat fusion.sql)"

# --- Start only pgAdmin ---
.PHONY: pgadmin
pgadmin:
	@echo "📊 Starting pgAdmin"
	docker-compose -f $(docker_compose_file) up -d pgadmin

# --- Open application container shell ---
.PHONY: shell
shell:
	@echo "🐚 Opening shell in 'app' container"
	docker-compose -f $(docker_compose_file) exec app sh

# --- Run Mustache analysis ---
.PHONY: mustache
mustache:
	@echo "📊 Generating Mustache plots"
	docker-compose -f $(docker_compose_file) exec app python mustache.py

# --- Show logs ---
.PHONY: logs
logs:
	@echo "📋 Showing logs"
	docker-compose -f $(docker_compose_file) logs -f

# --- Check database status ---
.PHONY: check-db
check-db:
	@echo "🔍 Checking PostgreSQL status"
	docker-compose -f $(docker_compose_file) exec db pg_isready
