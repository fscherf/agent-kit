PYTHON=python3.14
PYTHON_ENV=.venv
PYPIRC=~/.pypirc.fscherf

.PHONY: all docker-build python-shell python-build clean build _pypi-upload

define DOCKER_COMPOSE_RUN
	docker compose run \
		-it \
		--user=$$(id -u):$$(id -g) \
		--remove-orphans \
		--service-ports \
		$1 $2
endef

all: python-shell

# docker
docker-build:
	docker compose build --no-cache ${args}

# python
python-shell:
	$(call DOCKER_COMPOSE_RUN,python)

python-bash:
	$(call DOCKER_COMPOSE_RUN,python,bash)

python-build:
	rm -rf build dist *.egg-info && \
	$(call DOCKER_COMPOSE_RUN,python,${PYTHON} -m build)

# meta
clean:
	rm -rf .venv build dist *.egg-info

build: docker-build python-build

# releases
_pypi-upload:
	$(call DOCKER_COMPOSE_RUN,-v ${PYPIRC}:/.pypirc,python twine upload --config-file /.pypirc dist/* --verbose)
