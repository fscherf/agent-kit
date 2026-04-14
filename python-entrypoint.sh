#!/bin/bash
set -e

PYTHON=python3.14
PYTHON_VENV=.venv

if ! [ -d "$PYTHON_VENV" ]; then
	$PYTHON -m venv $PYTHON_VENV && \
	source $PYTHON_VENV/bin/activate && \
	pip install pip --upgrade && \
	pip install -e .
else
	source $PYTHON_VENV/bin/activate
fi

exec /bin/bash
