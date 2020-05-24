import json
import os
import pickle
import tempfile
from contextlib import contextmanager
from typing import Any, Generator, Optional, Union

import mlflow
import numpy as np
import pandas as pd
import plotly
import yaml
from matplotlib import pyplot as plt
from plotly import graph_objects as go

from mlflow_extend import plotting as mplt
from mlflow_extend.typing import ArrayLike
from mlflow_extend.utils import flatten_dict

__all__ = [
    "log_params_flatten",
    "log_metrics_flatten",
    "log_plt_figure",
    "log_plotly_figure",
    "log_figure",
    "log_dict",
    "log_df",
    "log_text",
    "log_numpy",
    "log_confusion_matrix",
    "log_feature_importance",
    "log_roc_curve",
    "log_pr_curve",
]


@contextmanager
def _artifact_context(path: str) -> Generator[str, None, None]:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.normpath(path)
        dirname = os.path.dirname(path)
        filename = os.path.basename(path)
        artifact_path = None if dirname == filename else dirname
        path = os.path.join(tmpdir, filename)
        yield path
        mlflow.log_artifact(path, artifact_path)


def log_params_flatten(params: dict, parent_key: str = "", sep: str = ".") -> None:
    """
    Log a batch of params after flattening.

    Parameters
    ----------
    params : dict
        Dictionary of parameters to log.
    parent_key : str, default ""
        Parent key.
    sep : str, default "."
        Key separator.

    Returns
    -------
    None
        None

    Examples
    --------
    >>> with mlflow.start_run() as run:
    ...     params = {"a": {"b": 0}}
    ...     mlflow.log_params_flatten(params)
    ...     mlflow.log_params_flatten(params, parent_key="d")
    ...     mlflow.log_params_flatten(params, sep="_")
    >>> r = mlflow.get_run(run.info.run_id)
    >>> sorted(r.data.params.items())
    [('a.b', '0'), ('a_b', '0'), ('d.a.b', '0')]

    """
    mlflow.log_params(flatten_dict(params, parent_key, sep))


def log_metrics_flatten(
    metrics: dict, step: Optional[int] = None, parent_key: str = "", sep: str = ".",
) -> None:
    """
    Log a batch of metrics after flattening.

    Parameters
    ----------
    metrics : dict
        Dictionary of metrics to log.
    step : int, default None
        Metric step. Defaults to zero if unspecified.
    parent_key : str, default ""
        Parent key.
    sep : str, default "."
        Key separator.

    Returns
    -------
    None
        None

    Examples
    --------
    >>> with mlflow.start_run() as run:
    ...     metrics = {"a": {"b": 0.0}}
    ...     mlflow.log_metrics_flatten(metrics)
    ...     mlflow.log_metrics_flatten(metrics, parent_key="d")
    ...     mlflow.log_metrics_flatten(metrics, sep="_")
    >>> r = mlflow.get_run(run.info.run_id)
    >>> sorted(r.data.metrics.items())
    [('a.b', 0.0), ('a_b', 0.0), ('d.a.b', 0.0)]

    """
    mlflow.log_metrics(flatten_dict(metrics, parent_key, sep), step)


def log_plt_figure(fig: plt.Figure, path: str) -> None:
    """
    Log a matplotlib figure as an artifact.

    Parameters
    ----------
    fig : matplotlib.pyplot.Figure
        Figure to log.
    path : str
        Path in the artifact store.

    Returns
    -------
    None
        None

    Examples
    --------
    >>> with mlflow.start_run() as run:
    ...     fig, ax = plt.subplots()
    ...     _ = ax.plot([0, 1], [0, 1])
    ...     mlflow.log_figure(fig, 'plt_figure.png')
    >>> list_artifacts(run.info.run_id)
    ['plt_figure.png']

    """
    with _artifact_context(path) as tmp_path:
        fig.savefig(tmp_path)
        plt.close(fig)


def log_plotly_figure(fig: go.Figure, path: str) -> None:
    """
    Log a plotly figure as an artifact.

    Parameters
    ----------
    fig : go.Figure
        Figure to log.
    path : str
        Path in the artifact store.

    Returns
    -------
    None
        None

    Examples
    --------
    >>> with mlflow.start_run() as run:
    ...     fig = go.Figure(data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])])
    ...     mlflow.log_figure(fig, 'plotly_figure.html')  # Must be an HTML file.
    >>> list_artifacts(run.info.run_id)
    ['plotly_figure.html']

    """
    if not path.endswith("html"):
        raise ValueError('"{}" is not an HTML file.'.format(os.path.basename(path)))

    with _artifact_context(path) as tmp_path:
        plotly.offline.plot(
            fig, filename=tmp_path, include_plotlyjs="cdn", auto_open=False
        )


def log_figure(fig: Union[plt.Figure, go.Figure], path: str) -> None:
    """
    Log a matplotlib figure as an artifact.

    Parameters
    ----------
    fig : matplotlib.pyplot.Figure or plotly.graph_objects.Figure
        Figure to log.
    path : str
        Path in the artifact store.

    Returns
    -------
    None
        None

    Examples
    --------
    Matplotlib

    >>> with mlflow.start_run() as run:
    ...     fig, ax = plt.subplots()
    ...     _ = ax.plot([0, 1], [0, 1])
    ...     mlflow.log_figure(fig, 'plt_figure.png')
    >>> list_artifacts(run.info.run_id)
    ['plt_figure.png']

    Plotly

    >>> with mlflow.start_run() as run:
    ...     fig = go.Figure(data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])])
    ...     mlflow.log_figure(fig, 'plotly_figure.html')  # Must be an HTML file.
    >>> list_artifacts(run.info.run_id)
    ['plotly_figure.html']

    """
    if isinstance(fig, plt.Figure):
        log_plt_figure(fig, path)
    elif isinstance(fig, go.Figure):
        log_plotly_figure(fig, path)
    else:
        raise TypeError('Invalid figure type: "{}"'.format(type(fig)))


def log_dict(dct: dict, path: str, fmt: Optional[str] = None) -> None:
    """
    Log a dictionary as an artifact.

    Parameters
    ----------
    dct : dict
        Dictionary to log.
    path : str
        Path in the artifact store.
    fmt : str, default None
        File format to save dict in. If None, file format is inferred from `path`.

    Returns
    -------
    None
        None

    Examples
    --------
    >>> with mlflow.start_run() as run:
    ...     d = {'a': 0}
    ...     mlflow.log_dict(d, 'dict.json')
    ...     mlflow.log_dict(d, 'dict.yaml')
    ...     mlflow.log_dict(d, 'dict.yml')
    >>> list_artifacts(run.info.run_id)
    ['dict.json', 'dict.yaml', 'dict.yml']

    """
    fmt = os.path.splitext(path)[-1] if fmt is None else fmt
    fmt = fmt.lstrip(".")

    with _artifact_context(path) as tmp_path:
        with open(tmp_path, "w") as f:
            if fmt == "json":
                json.dump(dct, f, indent=2)
            elif fmt in ["yaml", "yml"]:
                yaml.dump(dct, f, default_flow_style=False)
            else:
                raise ValueError("Invalid file format: {}.".format(fmt))


def log_pickle(obj: Any, path: str) -> None:
    """
    Log a pickled object as an artifact.

    Parameters
    ----------
    obj : object
        Picklable object.
    path : str
        Path in the artifact store.

    Returns
    -------
    None
        None

    """
    with _artifact_context(path) as tmp_path:
        with open(tmp_path, mode="wb") as f:
            pickle.dump(obj, f)


def log_df(df: pd.DataFrame, path: str, fmt: str = "csv") -> None:
    """
    Log a dataframe as an artifact.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to log.
    path : str
        Path in the artifact store.
    fmt : str, default "csv"
        File format to save the dataframe in.

    Returns
    -------
    None
        None

    Examples
    --------
    >>> with mlflow.start_run() as run:
    ...     mlflow.log_df(pd.DataFrame({'a': [0]}), 'df.csv')
    >>> list_artifacts(run.info.run_id)
    ['df.csv']

    """
    with _artifact_context(path) as tmp_path:
        if fmt == "csv":
            df.to_csv(tmp_path, index=False)
        elif fmt == "feather":
            df.to_feather(tmp_path)
        else:
            raise ValueError("Invalid file format: {}.".format(fmt))


def log_text(text: str, path: str) -> None:
    """
    Log a text as an artifact.

    Parameters
    ----------
    text : str
        Text to log.
    path : str
        Path in the artifact store.

    Returns
    -------
    None
        None

    Examples
    --------
    >>> with mlflow.start_run() as run:
    ...     mlflow.log_text('text', 'text.txt')
    >>> list_artifacts(run.info.run_id)
    ['text.txt']

    """
    with _artifact_context(path) as tmp_path:
        with open(tmp_path, "w") as f:
            f.write(text)


def log_numpy(arr: np.ndarray, path: str) -> None:
    """
    Log a numpy array as an artifact.

    Parameters
    ----------
    arr : numpy.ndarray
        Numpy array to log.
    path : str
        Path in the artifact store.

    Returns
    -------
    None
        None

    Examples
    --------
    >>> with mlflow.start_run() as run:
    ...     mlflow.log_numpy(np.array([0]), 'array.npy')
    >>> list_artifacts(run.info.run_id)
    ['array.npy']

    """
    with _artifact_context(path) as tmp_path:
        np.save(tmp_path, arr)


def log_confusion_matrix(cm: ArrayLike, path: str = "confusion_matrix.png") -> None:
    """
    Log a confusion matrix as an artifact.

    Parameters
    ----------
    cm : array-like
        Confusion matrix to log.
    path : str, default "confusion_matrix.png"
        Path in the artifact store.

    Returns
    -------
    None
        None

    Examples
    --------
    >>> with mlflow.start_run() as run:
    ...     mlflow.log_confusion_matrix([[1, 2], [3, 4]])
    >>> list_artifacts(run.info.run_id)
    ['confusion_matrix.png']

    """
    fig = mplt.confusion_matrix(cm)
    log_figure(fig, path)


def log_feature_importance(
    features: ArrayLike,
    importances: ArrayLike,
    importance_type: str,
    limit: Optional[int] = None,
    normalize: bool = False,
    path: str = "feature_importance.png",
) -> None:
    """
    Log feature importance as an artifact.

    Parameters
    ----------
    features : array-like
        Feature names.
    importances : array-like
        Importance of each feature.
    importance_type : str
        Importance type (e.g. "gain").
    path : str, default "feature_importance.png"
        Path in the artifact store.
    **kwargs : dict
        Keyword arguments passed to mlflow.plotting.feature_importance.

    Returns
    -------
    None
        None

    Examples
    --------
    >>> with mlflow.start_run() as run:
    ...     features = ['a', 'b', 'c']
    ...     importances = [1, 2, 3]
    ...     mlflow.log_feature_importance(features, importances, 'gain')
    >>> list_artifacts(run.info.run_id)
    ['feature_importance.png']

    """
    fig = mplt.feature_importance(
        features, importances, importance_type, limit, normalize
    )
    log_figure(fig, path)


def log_roc_curve(
    fpr: ArrayLike,
    tpr: ArrayLike,
    auc: Optional[float] = None,
    path: str = "roc_curve.png",
) -> None:
    """
    Log ROC curve as an artifact.

    Parameters
    ----------
    fpr : array-like
        False positive rate.
    tpr : array-like
        True positive rate.
    auc : float, default None
        Area under the curve.
    path : str, default "roc_curve.png"
        Path in the artifact store.

    Returns
    -------
    None
        None

    Examples
    --------
    >>> with mlflow.start_run() as run:
    ...     mlflow.log_roc_curve([0, 1], [0, 1])
    >>> list_artifacts(run.info.run_id)
    ['roc_curve.png']

    """
    fig = mplt.roc_curve(fpr, tpr, auc)
    log_figure(fig, path)


def log_pr_curve(
    pre: ArrayLike,
    rec: ArrayLike,
    auc: Optional[float] = None,
    path: str = "pr_curve.png",
) -> None:
    """
    Log precision-recall curve as an artifact.

    Parameters
    ----------
    pre : array-like
        Precision.
    rec : array-like
        Recall.
    auc : float, default None
        Area under the curve.
    path : str, default "pr_curve.png"
        Path in the artifact store.

    Returns
    -------
    None
        None

    Examples
    --------
    >>> with mlflow.start_run() as run:
    ...     mlflow.log_pr_curve([1, 0], [1, 0])
    >>> list_artifacts(run.info.run_id)
    ['pr_curve.png']

    """
    fig = mplt.pr_curve(pre, rec, auc)
    log_figure(fig, path)
