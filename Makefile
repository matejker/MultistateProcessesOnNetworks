.PHONY: requirements requirements_tools requirements_test lint test

TEST_PATH=./tests

requirements:
	pip install -r requirements/base.txt

requirements_tools:
	pip install -r requirements/tools.txt

requirements_test:
	pip install -r requirements/test.txt

lint: requirements_tools
	flake8 --exclude=env,venv

test: requirements_test
ifndef TEST_ONLY
	TEST_ONLY=$(TEST_PATH)
endif
	python -m pytest -s -vv --color=yes $(TEST_ONLY)
