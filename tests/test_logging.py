import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mlflow_extend import mlflow
from mlflow_extend.logging import _artifact_context

from tests.utils import assert_file_exists_in_artifacts


@pytest.mark.parametrize("path", ["test.txt", "dir/test.txt", "dir/dir/test.txt"])
def test_artifact_context(path):
    with mlflow.start_run() as run:
        with _artifact_context(path) as tmp_path:
            open(tmp_path, "w").close()
        assert_file_exists_in_artifacts(run, path)


def test_log_figure():
    path = "test.png"
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    with mlflow.start_run() as run:
        mlflow.log_figure(fig, path)
        assert_file_exists_in_artifacts(run, path)


def test_log_dict():
    path = "test.json"
    with mlflow.start_run() as run:
        mlflow.log_dict({"a": 0}, path)
        assert_file_exists_in_artifacts(run, path)


def test_log_df():
    path = "test.csv"
    with mlflow.start_run() as run:
        mlflow.log_df(pd.DataFrame({"a": [0]}), path)
        assert_file_exists_in_artifacts(run, path)


def test_log_text():
    path = "test.txt"
    with mlflow.start_run() as run:
        mlflow.log_text("test", path)
        assert_file_exists_in_artifacts(run, path)


def test_log_numpy():
    path = "test.npy"
    with mlflow.start_run() as run:
        mlflow.log_numpy(np.array([0]), path)
        assert_file_exists_in_artifacts(run, path)


@pytest.mark.parametrize("path", [None, "cm.png"])
def test_log_confusion_matrix(path):
    with mlflow.start_run() as run:
        mlflow.log_confusion_matrix([[1, 2], [3, 4]], path)
        assert_file_exists_in_artifacts(run, path or "confusion_matrix.png")


@pytest.mark.parametrize("path", [None, "fi.png"])
def test_log_feature_importance(path):
    with mlflow.start_run() as run:
        mlflow.log_feature_importance(["a", "b", "c"], [1, 2, 3], "gain", path)
        assert_file_exists_in_artifacts(run, path or "feature_importance.png")


@pytest.mark.parametrize("limit", [2, 4])
def test_log_feature_importance_with_limit(limit):
    with mlflow.start_run() as run:
        mlflow.log_feature_importance(["a", "b", "c"], [1, 2, 3], "gain", limit=limit)
        assert_file_exists_in_artifacts(run, "feature_importance.png")


@pytest.mark.parametrize("normalize", [False, True])
def test_log_feature_importance_with_normalize(normalize):
    with mlflow.start_run() as run:
        mlflow.log_feature_importance(
            ["a", "b", "c"], [1, 2, 3], "gain", normalize=normalize
        )
        assert_file_exists_in_artifacts(run, "feature_importance.png")
