# https://stackoverflow.com/questions/10858261/how-to-abort-makefile-if-variable-not-set
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))

format:
	poetry run black validmind

lint:
	poetry run flake8 validmind

# Quick target to run all checks
check: format lint test

build:
	poetry build

test:
	poetry run python -m unittest discover tests

docs-html:
	poetry run sphinx-build -M html docs/ docs/_build

docs-markdown:
	poetry run sphinx-build -M markdown docs/ docs/_build

docs: docs-html docs-markdown

version:
	@:$(call check_defined, tag, new semver version tag to use on pyproject.toml)
	poetry version $(tag)
