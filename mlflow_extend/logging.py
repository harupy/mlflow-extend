import json
import os
import pickle
import tempfile
from contextlib import contextmanager
from typing import Any, Generator, Optional

import mlflow
import numpy as np
import pandas as pd
import yaml
from matplotlib import pyplot as plt

from mlflow_extend import plotting as mplt
from mlflow_extend.typing import ArrayLike
from mlflow_extend.utils import flatten_dict

__all__ = [
    "log_params_flatten",
    "log_metrics_flatten",
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
    Log a batch of params after flattening.

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


def log_figure(fig: plt.Figure, path: str) -> None:
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

    Examples
    --------
    >>> with mlflow.start_run():
    ...     fig, ax = plt.subplots()
    ...     _ = ax.plot([0, 1], [0, 1])
    ...     mlflow.log_figure(fig, 'figure.png')

    """
    with _artifact_context(path) as tmp_path:
        fig.savefig(tmp_path)
        plt.close(fig)


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

    Examples
    --------
    >>> with mlflow.start_run():
    ...     d = {'a': 0}
    ...     mlflow.log_dict(d, 'dict.json')
    ...     mlflow.log_dict(d, 'dict.yaml')
    ...     mlflow.log_dict(d, 'dict.yml')

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

    """
    with _artifact_context(path) as tmp_path:
        with open(tmp_path, mode="wb") as f:
            pickle.dump(obj, f)


def log_df(df: pd.DataFrame, path: str, fmt: str = "csv") -> None:
    """
    Log a dataframe as an artifact.

    Parameters
    ----------
    df : dict
        Dataframe to log.
    path : str
        Path in the artifact store.
    fmt : str, default "csv"
        File format to save the dataframe in.

    Returns
    -------
    None

    Examples
    --------
    >>> with mlflow.start_run():
    ...     mlflow.log_df(pd.DataFrame({'a': [0]}), 'df.csv')

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

    Examples
    --------
    >>> with mlflow.start_run():
    ...     mlflow.log_text('text', 'text.txt')

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

    Examples
    --------
    >>> with mlflow.start_run():
    ...     mlflow.log_numpy(np.array([0]), 'array.npy')

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

    Examples
    --------
    >>> with mlflow.start_run():
    ...     mlflow.log_confusion_matrix([[1, 2], [3, 4]])

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

    Examples
    --------
    >>> with mlflow.start_run():
    ...     features = ['a', 'b', 'c']
    ...     importances = [1, 2, 3]
    ...     mlflow.log_feature_importance(features, importances, 'gain')

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

    Examples
    --------
    >>> with mlflow.start_run():
    ...     mlflow.log_roc_curve([0, 1], [0, 1])

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

    Examples
    --------
    >>> with mlflow.start_run():
    ...     mlflow.log_pr_curve([1, 0], [1, 0])

    """
    fig = mplt.pr_curve(pre, rec, auc)
    log_figure(fig, path)
