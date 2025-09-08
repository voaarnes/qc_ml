.PHONY: help install install-dev test lint format clean run-api notebook docs

help:
	@echo "Available commands:"
	@echo "  make install      - Install project dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linting"
	@echo "  make format      - Format code"
	@echo "  make clean       - Clean temporary files"
	@echo "  make run-api     - Run FastAPI server"
	@echo "  make notebook    - Start Jupyter notebook"
	@echo "  make docs        - Generate documentation"

install:
	pip install --upgrade pip
	pip install -e .

install-dev:
	pip install --upgrade pip
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/ tests/
	mypy src/ --ignore-missing-imports
	black --check src/ tests/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info
	rm -rf .coverage htmlcov/
	rm -rf .pytest_cache/

run-api:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

notebook:
	jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

docs:
	sphinx-build -b html docs/ docs/_build/html
