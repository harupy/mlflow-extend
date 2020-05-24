# MLflow Extend

[![Documentation Status](https://readthedocs.org/projects/mlflow-extend/badge/?version=latest)](https://mlflow-extend.readthedocs.io/en/latest/?badge=latest)
[![CI](https://github.com/harupy/mlflow-extend/workflows/CI/badge.svg?event=push)](https://github.com/harupy/mlflow-extend/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/harupy/mlflow-extend/branch/master/graph/badge.svg)](https://codecov.io/gh/harupy/mlflow-extend)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/harupy/mlflow-extend.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/harupy/mlflow-extend/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/harupy/mlflow-extend.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/harupy/mlflow-extend/context:python)
[![version](https://img.shields.io/pypi/v/mlflow-extend?color=brightgreen)](https://pypi.org/project/mlflow-extend/)
![pyversions](https://img.shields.io/pypi/pyversions/mlflow-extend?color=brightgreen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub](https://img.shields.io/github/license/harupy/mlflow-extend?color=brightgreen)

Extend MLflow's functionality.

## Installation

From PyPI

```bash
pip install mlflow-extend
```

From GitHub (development version)

```
pip install git+https://github.com/harupy/mlflow-extend.git
```

## Example

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from plotly import graph_objects as go

from mlflow_extend import mlflow

with mlflow.start_run():
    # mlflow native APIs
    mlflow.log_param('param', 0)
    mlflow.log_metric('metric', 1.0)

    ##### new APIs mlflow_extend provides #####

    # flatten dict
    mlflow.log_params_flatten({"a": {"b": 0}})
    mlflow.log_metrics_flatten({"a": {"b": 0.0}})

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

    # plotly figure
    fig = go.Figure(data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])])
    mlflow.log_figure(fig, 'figure.html')

    # confusion matrix
    mlflow.log_confusion_matrix([[1, 2], [3, 4]])

    # run "mlflow ui" and see the result.
```
