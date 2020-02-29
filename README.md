# MLflow Extend

[![CI](https://github.com/harupy/mlflow-extend/workflows/CI/badge.svg?event=push)](https://github.com/harupy/mlflow-extend/actions?query=workflow%3ACI)
[![Documentation Status](https://readthedocs.org/projects/mlflow-extend/badge/?version=latest)](https://mlflow-extend.readthedocs.io/en/latest/?badge=latest)
[![version](https://img.shields.io/pypi/v/mlflow-extend?color=brightgreen)](https://pypi.org/project/mlflow-extend/)
![pyversions](https://img.shields.io/pypi/pyversions/mlflow-extend?color=brightgreen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub](https://img.shields.io/github/license/harupy/mlflow-extend?color=brightgreen)

Extend MLflow's functionality.

## Installation

```bash
pip install mlflow-extend
```

## Examples

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mlflow_extend import mlflow

with mlflow.start_run():
    # mlflow native APIs
    mlflow.log_param('param', 0)
    mlflow.log_metric('metric', 1.0)

    ##### new APIs mlflow_extend provides #####

    # dict
    mlflow.log_dict({'a': 0}, 'dict.json')

    # numpy array
    mlflow.log_numpy(np.array([0]), 'array.npy')

    # pandas dataframe
    mlflow.log_df(pd.DataFrame({'a': [0]}), 'df.csv')

    # matplotlib figure
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    mlflow.log_figure(fig, 'figure.png')

    # confusion matrix
    mlflow.log_confusion_matrix([[1, 2], [3, 4]])
```

## Creating Environment

```bash
conda create -n mlflow-extend python=3.6
conda activate mlflow-extend
pip install -r requirements.txt -r requirements-dev.txt
```

## Running Lint

```bash
# Run lint checking with black and flake8.
./dev/lint.sh
```

## Running type check

```bash
mypy .
```

## Running Test

```bash
# Run all the tests.
./dev/test.sh

# Save figures generated during the tests in '.pytest_basetemp'.
./dev/test.sh --savefig
```

## Building Documentation

```bash
cd docs
make html

# Remove everything under 'docs/build' and run 'make html'.
make clean html
```

The generated files will be stored in `docs/build/html`. Open `docs/build/html/index.html` on the browser to check if the documentation is built properly.
