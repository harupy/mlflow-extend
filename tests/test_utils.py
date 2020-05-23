from mlflow_extend import utils


def test_flatten_dict() -> None:
    dct = {"a": {"b": "c"}}
    assert utils.flatten_dict(dct) == {"a.b": "c"}
    assert utils.flatten_dict(dct, parent_key="d") == {"d.a.b": "c"}
    assert utils.flatten_dict(dct, sep="_") == {"a_b": "c"}
