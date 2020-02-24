import pytest
import numpy as np
import matplotlib.pyplot as plt

import mlflow_extend.plotting as mplt


def assert_is_figure(obj):
    assert isinstance(obj, plt.Figure)


@pytest.mark.parametrize("cm", [[[1, 2], [3, 4]], np.array([[1, 2], [3, 4]])])
def test_confusion_matrix(tmpdir, cm):
    fig = mplt.confusion_matrix(cm)
    assert_is_figure(fig)


@pytest.mark.parametrize("corr", [[[1, 2], [3, 4]], np.array([[1, 2], [3, 4]])])
def test_corr_matrix(tmpdir, corr):
    fig = mplt.corr_matrix(corr)
    assert_is_figure(fig)


def test_feature_importance(tmpdir):
    features = ["a", "b", "c"]
    importances = [1, 2, 3]
    importance_type = "gain"
    fig = mplt.feature_importance(features, importances, importance_type)
    assert_is_figure(fig)


@pytest.mark.parametrize("limit", [2, 3, 4])
def test_feature_importance_with_limit(tmpdir, limit):
    features = ["a", "b", "c"]
    importances = [1, 2, 3]
    importance_type = "gain"
    fig = mplt.feature_importance(features, importances, importance_type, limit)
    assert_is_figure(fig)


def test_feature_importance_with_normalize(tmpdir):
    features = ["a", "b", "c"]
    importances = [1, 2, 3]
    importance_type = "gain"
    fig = mplt.feature_importance(
        features, importances, importance_type, normalize=True
    )
    assert_is_figure(fig)


def test_roc_curve(tmpdir):
    fig = mplt.roc_curve([1, 2, 3], [1, 2, 3])
    assert_is_figure(fig)

    fig = mplt.roc_curve([1, 2, 3], [1, 2, 3], 0.5)
    assert_is_figure(fig)


def test_pr_curve(tmpdir):
    fig = mplt.pr_curve([1, 2, 3], [1, 2, 3])
    assert_is_figure(fig)

    fig = mplt.pr_curve([1, 2, 3], [1, 2, 3], 0.5)
