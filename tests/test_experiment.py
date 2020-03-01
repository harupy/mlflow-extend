import mlflow

from mlflow_extend import experiment as exp
from mlflow_extend.testing.utils import assert_new_apis_do_not_conflict_native_apis


def test_new_apis_do_not_conflict_native_apis():
    assert_new_apis_do_not_conflict_native_apis(exp)


def test_get_or_create_experiment():
    expr_name = "test"
    expr_id = exp.get_or_create_experiment(expr_name)

    expr = mlflow.get_experiment(expr_id)

    assert expr.experiment_id == expr_id
    assert expr.name == expr_name
