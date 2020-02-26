import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mlflow
import mlflow_extend.logging as lg

from tests.utils import assert_file_exists_in_artifacts


def test_new_apis_do_not_conflict_native_apis():
    assert all(new_api not in mlflow.__all__ for new_api in lg.__all__)


@pytest.mark.parametrize("path", ["test.txt", "dir/test.txt", "dir/dir/test.txt"])
def test_artifact_context(path):
    with mlflow.start_run() as run:
        with lg._artifact_context(path) as tmp_path:
            open(tmp_path, "w").close()
        assert_file_exists_in_artifacts(run, path)


def test_log_figure():
    path = "test.png"
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    with mlflow.start_run() as run:
        lg.log_figure(fig, path)
        assert_file_exists_in_artifacts(run, path)


def test_log_dict():
    path = "test.json"
    with mlflow.start_run() as run:
        lg.log_dict({"a": 0}, path)
        assert_file_exists_in_artifacts(run, path)


def test_log_df():
    path = "test.csv"
    with mlflow.start_run() as run:
        lg.log_df(pd.DataFrame({"a": [0]}), path)
        assert_file_exists_in_artifacts(run, path)


def test_log_text():
    path = "test.txt"
    with mlflow.start_run() as run:
        lg.log_text("test", path)
        assert_file_exists_in_artifacts(run, path)


def test_log_numpy():
    path = "test.npy"
    with mlflow.start_run() as run:
        lg.log_numpy(np.array([0]), path)
        assert_file_exists_in_artifacts(run, path)


@pytest.mark.parametrize("path", [None, "cm.png"])
def test_log_confusion_matrix(path):
    with mlflow.start_run() as run:
        lg.log_confusion_matrix([[1, 2], [3, 4]], path)
        assert_file_exists_in_artifacts(run, path or "confusion_matrix.png")


@pytest.mark.parametrize("path", [None, "fi.png"])
def test_log_feature_importance(path):
    with mlflow.start_run() as run:
        lg.log_feature_importance(["a", "b", "c"], [1, 2, 3], "gain", path)
        assert_file_exists_in_artifacts(run, path or "feature_importance.png")


@pytest.mark.parametrize("limit", [2, 3, 4])
def test_log_feature_importance_with_limit(limit):
    with mlflow.start_run() as run:
        lg.log_feature_importance(["a", "b", "c"], [1, 2, 3], "gain", limit=limit)
        assert_file_exists_in_artifacts(run, "feature_importance.png")


def test_log_feature_importance_with_normalize():
    with mlflow.start_run() as run:
        lg.log_feature_importance(["a", "b", "c"], [1, 2, 3], "gain", normalize=True)
        assert_file_exists_in_artifacts(run, "feature_importance.png")


@pytest.mark.parametrize("path", [None, "roc.png"])
def test_log_roc_curve(path):
    with mlflow.start_run() as run:
        lg.log_roc_curve([1, 2, 3], [1, 2, 3], path=path)
        assert_file_exists_in_artifacts(run, path or "roc_curve.png")


def test_log_roc_curve_with_auc():
    with mlflow.start_run() as run:
        lg.log_roc_curve([1, 2, 3], [1, 2, 3], 0.5)
        assert_file_exists_in_artifacts(run, "roc_curve.png")


@pytest.mark.parametrize("path", [None, "roc.png"])
def test_log_pr_curve(path):
    with mlflow.start_run() as run:
        lg.log_pr_curve([1, 2, 3], [1, 2, 3], path=path)
        assert_file_exists_in_artifacts(run, path or "pr_curve.png")


def test_log_pr_curve_with_auc():
    with mlflow.start_run() as run:
        lg.log_pr_curve([1, 2, 3], [1, 2, 3], 0.5)
        assert_file_exists_in_artifacts(run, "pr_curve.png")