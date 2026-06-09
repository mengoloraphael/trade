.PHONY: help install dev test lint format clean docker-up docker-down db-init db-migrate

help:
	@echo "Trade AI - Makefile Commands"
	@echo ""
	@echo "Installation:"
	@echo "  make install          Install dependencies"
	@echo "  make dev              Install dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run              Run FastAPI server"
	@echo "  make test             Run tests"
	@echo "  make lint             Lint code"
	@echo "  make format           Format code"
	@echo ""
	@echo "Database:"
	@echo "  make db-init          Initialize database"
	@echo "  make db-migrate       Run migrations"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up        Start Docker Compose"
	@echo "  make docker-down      Stop Docker Compose"
	@echo "  make docker-logs      Show Docker logs"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Clean up cache files"

# Installation
install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install -e .

# Running
run:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v --cov=src

jupyter:
	jupyter lab

# Code Quality
lint:
	flake8 src tests
	pylint src

format:
	black src tests
	isort src tests

# Database
db-init:
	python -c "from src.database.session import init_db; init_db()"

db-migrate:
	alembic upgrade head

# Docker
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f app

docker-rebuild:
	docker-compose build --no-cache

# Cleanup
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

clean-all: clean
	docker-compose down -v
