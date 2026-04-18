#!/bin/bash
set -e

export PYTHON=python3.14
export PYTHON_VENV="/app/data/python/venvs/$PYTHON"

if ! [ -d "$(dirname $PYTHON_VENV)" ]; then
    mkdir -p $(dirname $PYTHON_VENV)
fi

if ! [ -d "$PYTHON_VENV" ]; then
	$PYTHON -m venv $PYTHON_VENV && \
	source $PYTHON_VENV/bin/activate && \
	pip install pip --upgrade && \
	pip install -e .
fi

exec /bin/bash --rcfile /app/bash/.bashrc
