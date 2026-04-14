#!/bin/bash
set -e
set -x

MODELS="qwen3.5:2b gemma4:e2b"

for model in $MODELS; do
    ollama pull $model
done
