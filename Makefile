
.PHONY: run install clean check run_builder run_inference runner_build runner_inference
.DEFAULT_GOAL := runner_inference

run_builder: install
	cd src; poetry run python3 runner_builder.py

run_inference: install
	cd src; poetry run python3 runner_inference.py

install: pyproject.toml
	poetry install

clean:
	rm -rf `find . -type d -name __pycache__`
	rm -rf .ruff_cache

check:
	poetry run flake8 src/
	#poetry run ruff check src/
	

format:
	poetry run black src/

runner_build: check run_builder clean

runner_inference: check run_inference clean