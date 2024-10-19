
.PHONY: run install clean check run_api runner_api
.DEFAULT_GOAL := runner_api

run_api: install
	cd app; poetry run python3 run.py

install: pyproject.toml
	poetry install

clean:
	rm -rf `find . -type d -name __pycache__`
	rm -rf .ruff_cache

check:
	poetry run flake8 app/
	#poetry run ruff check src/
	
format:
	poetry run isort app/
	poetry run black app/

runner_api: check run_api clean