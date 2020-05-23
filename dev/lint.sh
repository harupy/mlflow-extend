#!/usr/bin/env bash

exit_code=0

black --check .
exit_code=$(( $? | $exit_code ))

isort --check-only .
exit_code=$(( $? | $exit_code ))

flake8 .
exit_code=$(( $? | $exit_code ))

exit $exit_code
