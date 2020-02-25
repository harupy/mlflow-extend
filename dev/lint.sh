#!/usr/bin/env bash

exit_code=0

black --check .
[[ $? = 1 ]] && exit_code=1

flake8 .
[[ $? = 1 ]] && exit_code=1

exit $exit_code
