#!/usr/bin/env bash

python -m pip install --progress-bar --upgrade pip
pip install --progress-bar off -r requirements.txt -r requirements-dev.txt
