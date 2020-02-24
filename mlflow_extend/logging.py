import os
import json
import tempfile
from contextlib import contextmanager
import numpy as np
import matplotlib.pyplot as plt
import mlflow

import mlflow_extend.plotting as mplt


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
    with _artifact_context(path) as tmp_path:
        fig.savefig(tmp_path)
        plt.close(fig)


def log_dict(d, path):
    with _artifact_context(path) as tmp_path:
        with open(tmp_path, "w") as f:
            json.dump(d, f, indent=2)


def log_df(df, path):
    with _artifact_context(path) as tmp_path:
        df.to_csv(tmp_path, index=False)


def log_str(s, path):
    with _artifact_context(path) as tmp_path:
        with open(tmp_path, "w") as f:
            f.write(s)


def log_numpy(arr, path):
    with _artifact_context(path) as tmp_path:
        np.save(tmp_path, arr)


def log_confusion_matrix(cm, path="confusion_matrix.png"):
    fig = mplt.corr_matrix(cm)
    log_figure(fig, path)


def log_feature_importance(
    feature, importances, importance_type, path="feature_importance.png", **kwargs
):
    fig = mplt.feature_importance(feature, importances, importance_type, **kwargs)
    log_figure(fig, path)
