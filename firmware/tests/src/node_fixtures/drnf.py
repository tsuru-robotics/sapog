import pytest
from pyuavcan.application import make_node, NodeInfo

from make_registry import make_registry


@pytest.fixture(scope="class")
def prepared_node():
    registry01 = make_registry(7, use_all_interfaces=True)
    return make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)


@pytest.fixture(scope="class")
def prepared_double_redundant_node():
    registry01 = make_registry(7, use_all_interfaces=True)
    return make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)


def get_prepared_double_redundant_node():
    registry01 = make_registry(7, use_all_interfaces=True)
    return make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)
