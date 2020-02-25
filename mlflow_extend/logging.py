import os
import json
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


def log_dict(d, path):
    """
    Log a dictionary as an artifact.

    Parameters
    ----------
    d : dict
        Dictionary to log.
    path : str
        Path in the artifact store.

    Returns
    -------
    None

    Examples
    --------
    >>> with mlflow.start_run():
    ...     mlflow.log_dict({'a': 0}, 'dict.json')

    """
    with _artifact_context(path) as tmp_path:
        with open(tmp_path, "w") as f:
            json.dump(d, f, indent=2)


def log_df(df, path):
    """
    Log a dataframe as an artifact.

    Parameters
    ----------
    df : dict
        Dataframe to log.
    path : str
        Path in the artifact store.

    Returns
    -------
    None

    Examples
    --------
    >>> with mlflow.start_run():
    ...     mlflow.log_df(pd.DataFrame({'a': [0]}), 'df.csv')

    """
    with _artifact_context(path) as tmp_path:
        df.to_csv(tmp_path, index=False)


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


def log_confusion_matrix(cm, path=None):
    """
    Log a confusion matrix as an artifact.

    Parameters
    ----------
    cm : array-like
        Confusion matrix to log.
    path : str
        Path in the artifact store.

    Returns
    -------
    None

    Examples
    --------
    >>> with mlflow.start_run():
    ...     mlflow.log_confusion_matrix([[1, 2], [3, 4]])

    """
    path = "confusion_matrix.png" if path is None else path
    fig = mplt.corr_matrix(cm)
    log_figure(fig, path)


def log_feature_importance(features, importances, importance_type, path=None, **kwargs):
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
    path : str, default None
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
    path = "feature_importance.png" if path is None else path
    fig = mplt.feature_importance(features, importances, importance_type, **kwargs)
    log_figure(fig, path)
