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

build:
	poetry build

version:
	@:$(call check_defined, tag, new semver version tag to use on pyproject.toml)
	poetry version $(tag)
