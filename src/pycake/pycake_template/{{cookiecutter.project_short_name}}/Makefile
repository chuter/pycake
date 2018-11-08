.PHONY: clean clean-test clean-pyc clean-build docs dist
.DEFAULT_GOAL := help

init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

help:
	@echo make init
	@echo        prepare development environment, use only once
	@echo make clean
	@echo        remove all build, test, coverage and python artifacts
	@echo make ci
	@echo        run tests quickly with the default Python
	@echo make test-all
	@echo        run tests on every Python version with detox
	@echo make lint
	@echo        check style with flake8
	@echo make coverage
	@echo        check code coverage quickly with the default Python
	@echo make release
	@echo        package and upload a release
	@echo make dist
	@echo        builds source and wheel package
	@echo make install
	@echo        install the package to the active Python's site-packages

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint:
	pipenv run flake8 --exclude=.tox,*.egg,build,data .

pipenv-install: ## install the package to pipenv for test
	pipenv run python setup.py -q install

ci: pipenv-install
	pipenv run py.test -n 8 --junitxml=report.xml

test-all:
	pipenv run detox

coverage: pipenv-install
	pipenv run py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov={{ cookiecutter.project_short_name }} tests

release: lint dist
	pip install --upgrade twine
	twine check dist/*
	twine upload dist/*	

dist:
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel

install: clean
	python setup.py install
