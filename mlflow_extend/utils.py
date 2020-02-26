import yaml
import json


def to_json(data, path):
    """
    Write data to a JSON file.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def to_yaml(data, path):
    """
    Write data to a YAML file.
    """
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
