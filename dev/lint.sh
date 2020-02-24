#!/usr/bin/env bash

exit_code=0

black --check .
[[ ! $? = 0 ]] && exit_code=$?

flake8 .
[[ ! $? = 0 ]] && exit_code=$?

exit $exit_code
