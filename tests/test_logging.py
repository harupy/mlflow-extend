import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mlflow
import mlflow_extend.logging as lg

from mlflow_extend.testing.utils import (
    get_default_args,
    assert_file_exists_in_artifacts,
)


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


@pytest.mark.parametrize("path", ["test.json", "test.yaml", "test.yml"])
def test_log_dict(path):
    with mlflow.start_run() as run:
        lg.log_dict({"a": 0}, path)
        assert_file_exists_in_artifacts(run, path)


def test_log_pickle():
    with mlflow.start_run() as run:
        path = "test.pkl"
        lg.log_pickle({"a": 0}, path)
        assert_file_exists_in_artifacts(run, path)


@pytest.mark.parametrize("fmt", ["json", "yaml", "yml"])
def test_log_dict_with_fmt(fmt):
    with mlflow.start_run() as run:
        path = "test.{}".format(fmt)
        lg.log_dict({"a": 0}, path, fmt)
        assert_file_exists_in_artifacts(run, path)


@pytest.mark.parametrize("fmt", ["csv", "feather"])
def test_log_df(fmt):
    path = "test.csv"
    with mlflow.start_run() as run:
        lg.log_df(pd.DataFrame({"a": [0]}), path, fmt)
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


def test_log_confusion_matrix():
    default_path = get_default_args(lg.log_confusion_matrix)["path"]
    with mlflow.start_run() as run:
        lg.log_confusion_matrix([[1, 2], [3, 4]])
        assert_file_exists_in_artifacts(run, default_path)

    with mlflow.start_run() as run:
        path = "cm.png"
        lg.log_confusion_matrix([[1, 2], [3, 4]], path)
        assert_file_exists_in_artifacts(run, path)


def test_log_feature_importance():
    default_path = get_default_args(lg.log_feature_importance)["path"]
    with mlflow.start_run() as run:
        lg.log_feature_importance(["a", "b", "c"], [1, 2, 3], "gain")
        assert_file_exists_in_artifacts(run, default_path)

    with mlflow.start_run() as run:
        lg.log_feature_importance(["a", "b", "c"], [1, 2, 3], "gain", normalize=True)
        assert_file_exists_in_artifacts(run, default_path)

    with mlflow.start_run() as run:
        path = "feat_imp.png"
        lg.log_feature_importance(["a", "b", "c"], [1, 2, 3], "gain", path)
        assert_file_exists_in_artifacts(run, path)


@pytest.mark.parametrize("limit", [2, 3, 4])
def test_log_feature_importance_with_limit(limit):
    default_path = get_default_args(lg.log_feature_importance)["path"]
    with mlflow.start_run() as run:
        lg.log_feature_importance(["a", "b", "c"], [1, 2, 3], "gain", limit=limit)
        assert_file_exists_in_artifacts(run, default_path)


def test_log_roc_curve():
    default_path = get_default_args(lg.log_roc_curve)["path"]
    with mlflow.start_run() as run:
        lg.log_roc_curve([0, 1], [0, 1])
        assert_file_exists_in_artifacts(run, default_path)

    with mlflow.start_run() as run:
        lg.log_roc_curve([0, 1], [0, 1], 0.5)
        assert_file_exists_in_artifacts(run, default_path)

    with mlflow.start_run() as run:
        path = "roc.png"
        lg.log_roc_curve([0, 1], [0, 1], path=path)
        assert_file_exists_in_artifacts(run, path)


def test_log_pr_curve():
    default_path = get_default_args(lg.log_pr_curve)["path"]
    with mlflow.start_run() as run:
        lg.log_pr_curve([1, 0], [1, 0])
        assert_file_exists_in_artifacts(run, default_path)

    with mlflow.start_run() as run:
        lg.log_pr_curve([1, 0], [1, 0], 0.5)
        assert_file_exists_in_artifacts(run, default_path)

    with mlflow.start_run() as run:
        path = "pr.png"
        lg.log_pr_curve([1, 0], [1, 0], path=path)
        assert_file_exists_in_artifacts(run, path)
