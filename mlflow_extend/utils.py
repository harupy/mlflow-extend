def flatten_dict(dct: dict, parent_key: str = "", sep: str = ".") -> dict:
    """
    Flatten a nested dictionary.

    Parameters
    ----------
    dct : dict
        Dictionary to flatten.
    parent_key : str, default ""
        Parent key.
    sep : str, default "."
        Key separator.

    Examples
    --------
    >>> flatten_dict({"a": {"b": "c"}})
    {'a.b': 'c'}

    >>> flatten_dict({"a": {"b": "c"}}, parent_key="d")
    {'d.a.b': 'c'}

    >>> flatten_dict({"a": {"b": "c"}}, sep='_')
    {'a_b': 'c'}

    """
    items = []  # type: ignore
    for k, v in dct.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
