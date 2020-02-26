import os
import json
import yaml
import tempfile
from contextlib import contextmanager
import numpy as np
import matplotlib.pyplot as plt
import mlflow

import mlflow_extend.plotting as mplt

__all__ = [
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
def _artifact_context(path):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.normpath(path)
        dirname = os.path.dirname(path)
        filename = os.path.basename(path)
        artifact_path = None if dirname == filename else dirname
        path = os.path.join(tmpdir, filename)
        yield path
        mlflow.log_artifact(path, artifact_path)


def log_figure(fig, path):
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


def log_dict(d, path, fmt=None):
    """
    Log a dictionary as an artifact.

    Parameters
    ----------
    d : dict
        Dictionary to log.
    path : str
        Path in the artifact store.
    fmt : str, default None
        File format to save dict in. If None, format file is inferred from `path`.

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
    fmt = os.path.splitext(path)[1:] if fmt is None else fmt

    with _artifact_context(path) as tmp_path:
        with open(tmp_path, "w") as f:
            if fmt == "json":
                json.dump(d, f, indent=2)

            if fmt in ["yaml", "yml"]:
                yaml.dump(d, f, default_flow_style=False)


def log_df(df, path, fmt="csv"):
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
            raise ValueError("Invalid format: {}.".format(fmt))


def log_text(text, path):
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


def log_numpy(arr, path):
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


def log_confusion_matrix(cm, path="confusion_matrix.png"):
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
    fig = mplt.corr_matrix(cm)
    log_figure(fig, path)


def log_feature_importance(
    features, importances, importance_type, path="feature_importance.png", **kwargs
):
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
    fig = mplt.feature_importance(features, importances, importance_type, **kwargs)
    log_figure(fig, path)


def log_roc_curve(fpr, tpr, auc=None, path="roc_curve.png"):
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


def log_pr_curve(pre, rec, auc=None, path="pr_curve.png"):
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
