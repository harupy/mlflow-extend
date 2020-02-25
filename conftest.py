"""
Make sure this file is in the project root so that pytest adds the root to PYTHONPATH
when running the tests.
"""

import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mlflow_extend.mlflow


def pytest_addoption(parser):
    parser.addoption(
        "--savefig",
        action="store_true",
        default=False,
        help="Save figures when testing the plot functions.",
    )


@pytest.fixture(autouse=True)
def inject_items_into_doctest_namespace(doctest_namespace):
    doctest_namespace["np"] = np
    doctest_namespace["pd"] = pd
    doctest_namespace["plt"] = plt
    doctest_namespace["mlflow"] = mlflow_extend.mlflow


@pytest.fixture(scope="function", autouse=True)
def save_figure(request, tmpdir):
    """
    Save a matplotlib figure when "--savefig" is enabled.
    """
    yield
    if request.config.getoption("--savefig") and len(plt.get_fignums()) > 0:
        plt.gcf().savefig(tmpdir.join("test.png"))


@pytest.fixture(scope="function", autouse=True)
def close_figures():
    """
    Close all matplotlib figures.
    """
    yield
    plt.close("all")
