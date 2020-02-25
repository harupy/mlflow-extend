import os
from setuptools import setup, find_packages

import mlflow_extend

ROOT = os.path.abspath(os.path.dirname(__file__))


# Use README.md as a long description.
def get_long_description():
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
        return f.read()


def get_install_requires():
    with open(os.path.join(ROOT, "requirements.txt"), encoding="utf-8") as f:
        return [
            l.strip()
            for l in f.readlines()
            if not (l.startswith("#") or (l.strip() == ""))
        ]


setup(
    name="mlflow-extend",
    version=mlflow_extend.__version__,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=get_install_requires(),
    maintainer="harupy",
    maintainer_email="hkawamura0130@gmail.com",
    url="https://github.com/harupy/mlflow-extend",
    project_urls={
        "Documentation": "https://mlflow-extend.readthedocs.io/en/latest/index.html",
        "Source Code": "https://github.com/harupy/mlflow-extend",
        "Bug Tracker": "https://github.com/harupy/mlflow-extend/issues",
    },
    description="Extend MLflow API",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
)
