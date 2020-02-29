import matplotlib.pyplot as plt
import mlflow
import numpy as np
import pandas as pd
import pytest

import mlflow_extend.logging as lg
from mlflow_extend.testing.utils import (
    assert_file_exists_in_artifacts,
    get_default_args,
)


def test_new_apis_do_not_conflict_native_apis():
    assert all(new_api not in mlflow.__all__ for new_api in lg.__all__)


@pytest.mark.parametrize("path", ["test.txt", "dir/test.txt", "dir/dir/test.txt"])
def test_artifact_context(path):
    with mlflow.start_run() as run:
        with lg._artifact_context(path) as tmp_path:
            open(tmp_path, "w").close()
        assert_file_exists_in_artifacts(run, path)


def test_log_params_flatten():
    with mlflow.start_run() as run:
        params = {"a": {"b": 0}}
        lg.log_params_flatten(params)
        lg.log_params_flatten(params, parent_key="d")
        lg.log_params_flatten(params, sep="_")

    loaded_run = mlflow.get_run(run.info.run_id)
    assert loaded_run.data.params == {"a.b": "0", "a_b": "0", "d.a.b": "0"}


def test_log_metrics_flatten():
    with mlflow.start_run() as run:
        metrics = {"a": {"b": 0.0}}
        lg.log_metrics_flatten(metrics)
        lg.log_metrics_flatten(metrics, parent_key="d")
        lg.log_metrics_flatten(metrics, sep="_")

    loaded_run = mlflow.get_run(run.info.run_id)
    assert loaded_run.data.metrics == {"a.b": 0.0, "a_b": 0.0, "d.a.b": 0.0}


def test_log_figure():
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    with mlflow.start_run() as run:
        path = "test.png"
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
    with mlflow.start_run() as run:
        path = "test.csv"
        lg.log_df(pd.DataFrame({"a": [0]}), path, fmt)
        assert_file_exists_in_artifacts(run, path)


def test_log_text():
    with mlflow.start_run() as run:
        path = "test.txt"
        lg.log_text("test", path)
        assert_file_exists_in_artifacts(run, path)


def test_log_numpy():
    with mlflow.start_run() as run:
        path = "test.npy"
        lg.log_numpy(np.array([0]), path)
        assert_file_exists_in_artifacts(run, path)


def test_log_confusion_matrix():
    with mlflow.start_run() as run:
        default_path = get_default_args(lg.log_confusion_matrix)["path"]
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
        lg.log_feature_importance(["a", "b", "c"], [1, 2, 3], "gain", path=path)
        assert_file_exists_in_artifacts(run, path)


@pytest.mark.parametrize("limit", [2, 3, 4])
def test_log_feature_importance_with_limit(limit):
    with mlflow.start_run() as run:
        default_path = get_default_args(lg.log_feature_importance)["path"]
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
