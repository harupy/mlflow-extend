from setuptools import setup

import bare_pytest_raises
from version import __version__

setup(
    name="flake8-extensions",
    version=__version__,
    zip_safe=False,
    py_modules=["bare_pytest_raises"],
    install_requires=["flake8"],
    entry_points={
        "flake8.extension": [
            (
                f"{bare_pytest_raises.ERROR_CODE_PREFIX} "
                "= bare_pytest_raises:BarePytestRaises"
            )
        ]
    },
)
