#!/usr/bin/env bash

black --check .
isort --check-only .
flake8 .
