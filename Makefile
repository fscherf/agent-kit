PYPIRC=~/.pypirc.fscherf

.PHONY: \
	all clean build \
	docker-build docker-pull \
	ollama ollama-bash ollama-pull \
	python-shell python-build \
	_pypi-upload

define DOCKER_COMPOSE_UP
	docker compose up \
		--remove-orphans \
		$1
endef

define DOCKER_COMPOSE_RUN
	docker compose run \
		-it \
		--user=$$(id -u):$$(id -g) \
		--remove-orphans \
		--service-ports \
		$1 $2
endef

define DOCKER_COMPOSE_EXEC
	docker compose exec \
		-it \
		--user=$$(id -u):$$(id -g) \
		$1 $2
endef

# meta
all: python-shell

clean:
	rm -rf .venv build dist *.egg-info

build: docker-build python-build

# docker
docker-build:
	docker compose build --no-cache ${args}

docker-pull:
	docker compose pull

# ollama
ollama:
	$(call DOCKER_COMPOSE_UP,ollama)

ollama-bash:
	$(call DOCKER_COMPOSE_RUN,--entrypoint bash,ollama)

ollama-pull:
	$(call DOCKER_COMPOSE_EXEC,ollama,/app/ollama/pull.sh)

# python
python-shell:
	$(call DOCKER_COMPOSE_RUN,python)

python-bash:
	$(call DOCKER_COMPOSE_RUN,python,bash)

python-build:
	rm -rf build dist *.egg-info && \
	$(call DOCKER_COMPOSE_RUN,python,python -m build)

# releases
_pypi-upload:
	$(call DOCKER_COMPOSE_RUN,-v ${PYPIRC}:/.pypirc,python twine upload --config-file /.pypirc dist/* --verbose)
