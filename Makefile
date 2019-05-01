.PHONY: help compile-deps install-deps clean lint test dist

help:
	@echo "make compile-deps:"
	@echo "    update requirements.txt and requirements-dev.txt."
	@echo "make install-deps:"
	@echo "    install dev packages."
	@echo "make clean:"
	@echo "    clean extra files."
	@echo "make lint:"
	@echo "    check code using flake8."
	@echo "make test:"
	@echo "    test program."
	@echo "make dist:"
	@echo "    make a wheel package."
	@echo "make init-db:"
	@echo "    initial tables"

compile-deps:
	@[ -n "$(VIRTUAL_ENV)" ] || (echo 'out of virtualenv'; exit 1)
	@pip3 install -U pip setuptools wheel
	@pip3 install -U pip-tools
	@pip-compile --no-index -U requirements.in --output-file=requirements.txt
	@pip-compile --no-index -U requirements.in requirements-dev.in --output-file=requirements-dev.txt

install-deps:
	@[ -n "$(VIRTUAL_ENV)" ] || (echo 'out of virtualenv'; exit 1)
	@pip3 install -U pip setuptools wheel
	@pip3 install -r requirements-dev.txt

clean:
	@rm -rf dist build blog.egg-info htmlcov .pytest_cache
	@find . -name '__pycache__' | xargs rm -rf
	@find . -name '*.pyc' -or -name '*.pyo' -delete

lint:
	@[ -n "$(VIRTUAL_ENV)" ] || (echo 'out of virtualenv'; exit 1)
	@flake8

test:
	@[ -n "$(VIRTUAL_ENV)" ] || (echo 'out of virtualenv'; exit 1)
	coverage erase
	coverage run  -m pytest blog/tests/admin -p no:warnings
	coverage run -m pytest blog/tests/weblog -p no:warnings
	coverage report --omit=*tests* --include=blog*
	coverage html --omit=*tests* --include=blog*
	@rm -rf .pytest_cache

dist: clean
	@[ -n "$(VIRTUAL_ENV)" ] || (echo 'out of virtualenv'; exit 1)
	@python3 ./setup.py sdist bdist_wheel
	@rm -rf build

init-db:
	@python manager.py init-db
