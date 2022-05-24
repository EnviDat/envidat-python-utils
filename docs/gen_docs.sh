#!/bin/bash

pdm install -G docs
PYTHON_VERSION=$(cat ../pyproject.toml | grep requires-python | grep -Eo '[0-9]\.[0-9]+')
../__pypackages__/${PYTHON_VERSION}/bin/gendocs --config mkgendocs.yml
