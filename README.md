# MLflow Extend

[![Test](https://github.com/harupy/mlflow-extend/workflows/Test/badge.svg?event=push)](https://github.com/harupy/mlflow-extend/actions?query=workflow%3ATest)
[![Documentation Status](https://readthedocs.org/projects/mlflow-extend/badge/?version=latest)](https://mlflow-extend.readthedocs.io/en/latest/?badge=latest)
[![version](https://img.shields.io/pypi/v/mlflow-extend?color=brightgreen)](https://pypi.org/project/mlflow-extend/)
![pyversions](https://img.shields.io/pypi/pyversions/mlflow-extend?color=brightgreen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub](https://img.shields.io/github/license/harupy/mlflow-extend?color=brightgreen)

Extend MLflow's functionality.

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

## Lint

```bash
# Run lint checking with black and flake8.
./dev/lint.sh
```

## Test

```bash
# Run all the tests.
./dev/test.sh

# Save figures generated during the tests to ".pytest_basetemp".
./dev/test.sh --savefig
```

## Build Documentation

```bash
cd docs
make html  # or make clean html
```
