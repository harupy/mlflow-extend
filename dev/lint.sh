#!/usr/bin/env bash

flake8 .
isort --check-only .
black --check .
