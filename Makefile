.PHONY: install
install:
	@if conda env list | grep -q 'ai-baseballcoach'; then \
		conda env update -f environment.yml; \
	else \
		conda env create -f environment.yml; \
	fi
	pre-commit install && npm install && pip install .

.PHONY: test
test:
	python -m pytest -v

.PHONY: test_coverage
test_coverage:
	python -m pytest  -v --cov=app

.PHONY: test_debug
test_debug:
	python -m pytest -v -o log_cli=true

.PHONY: test_watch
test_watch:
	ptw

.PHONY: lint
lint:
	black . --check
	isort . --check
	cd app && pylint . --rcfile=../.pylintrc
	yamllint -c .yamllint .
	flake8 .
	npx textlint ./README.md

.PHONY: format
format:
	black .
	isort .

.PHONY: before_commit
before_commit: test format lint

.PHONY: run
run:
	ai-baseballcoach
