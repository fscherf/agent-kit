#!/bin/bash
set -e

PYTHON=python3.14
PYTHON_VENV="/app/data/python/$PYTHON.venv"

if ! [ -d "$(dirname $PYTHON_VENV)" ]; then
    mkdir -p $(dirname $PYTHON_VENV)
fi

if ! [ -d "$PYTHON_VENV" ]; then
	$PYTHON -m venv $PYTHON_VENV && \
	source $PYTHON_VENV/bin/activate && \
	pip install pip --upgrade && \
	pip install -e .
else
	source $PYTHON_VENV/bin/activate
fi

exec /bin/bash
