import pathlib

import pytest
import sys


@pytest.fixture(scope="session")
def add_deps2():
    source_path = pathlib.Path(__file__).parent.absolute()
    dependency_path = source_path.parent / "deps"
    namespace_path = dependency_path / "namespaces"
    print(f"Namespace path: {namespace_path.absolute()}")
    sys.path.insert(0, str(namespace_path.absolute()))


def add_deps():
    source_path = pathlib.Path(__file__).parent.absolute()
    dependency_path = source_path.parent / "deps"
    namespace_path = dependency_path / "namespaces"
    print(f"Namespace path: {namespace_path.absolute()}")
    sys.path.insert(0, str(namespace_path.absolute()))
