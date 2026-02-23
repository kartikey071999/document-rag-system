.PHONY: help install install-dev lint format test check clean run migrate

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install all dependencies including dev tools"
	@echo "  make lint         - Run ruff and black checks"
	@echo "  make format       - Format code with ruff and black"
	@echo "  make test         - Run tests with pytest"
	@echo "  make check        - Run Django checks"
	@echo "  make clean        - Remove build artifacts and cache"
	@echo "  make run          - Run Django development server"
	@echo "  make migrate      - Run Django migrations"

install:
	uv pip install -e .

install-dev:
	uv pip install -e ".[dev]"

lint:
	@echo "Running ruff check..."
	ruff check .
	@echo "Running ruff format check..."
	ruff format --check .
	@echo "Running black check..."
	black --check .

format:
	@echo "Formatting with ruff..."
	ruff check --fix .
	ruff format .
	@echo "Formatting with black..."
	black .

test:
	@echo "Running tests with pytest..."
	pytest -v

check:
	@echo "Running Django checks..."
	python manage.py check

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	rm -f coverage.xml bandit-report.json

run:
	python manage.py runserver

migrate:
	python manage.py migrate
