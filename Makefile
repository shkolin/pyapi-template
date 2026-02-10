ENV ?= prod
PYTHON := venv/bin/python

venv:
	python -m venv venv

setup_python: venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements/$(ENV).txt

migrate:
	$(PYTHON) -m alembic upgrade head

lint:
	$(PYTHON) -m ruff check app tests

typecheck:
	$(PYTHON) -m mypy app tests

functional_test:
	$(PYTHON) -m pytest tests/functional

unit_test:
	$(PYTHON) -m pytest tests/unit

tests: functional_test unit_test
