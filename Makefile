# https://stackoverflow.com/questions/10858261/how-to-abort-makefile-if-variable-not-set
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))

format:
	poetry run black validmind
	poetry run isort validmind

lint:
	poetry run flake8 validmind

install:
	poetry install --all-extras
	poetry run pre-commit install --hook-type pre-commit --hook-type pre-push

# Quick target to run all checks
check: copyright format lint test

build:
	poetry build

test:
	poetry run python -m unittest discover tests

test-integration:
	poetry run python scripts/run_e2e_notebooks.py

docs:
	poetry run pdoc validmind -d google -t docs/templates --no-show-source --logo https://vmai.s3.us-west-1.amazonaws.com/vm-logo.svg --favicon https://vmai.s3.us-west-1.amazonaws.com/favicon.ico -o docs/_build

docs-serve:
	poetry run pdoc validmind -d google -t docs/templates --no-show-source --logo https://vmai.s3.us-west-1.amazonaws.com/vm-logo.svg --favicon https://vmai.s3.us-west-1.amazonaws.com/favicon.ico

version:
	@:$(call check_defined, tag, new semver version tag to use on pyproject.toml)
	poetry version $(tag)
	echo "__version__ = \"$$(poetry version -s)\"" > validmind/__version__.py

copyright:
	poetry run python scripts/copyright_files.py

verify-copyright:
	poetry run python scripts/verify_copyright.py

verify-exposed-credentials:
	poetry run python scripts/ensure_clean_notebooks.py

ensure-clean-notebooks:
	poetry run python scripts/ensure_clean_notebooks.py

.PHONY: docs
