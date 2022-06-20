import pytest
from pyuavcan.application import make_node, NodeInfo

from make_registry import make_registry


@pytest.fixture()
def prepared_node():
    registry01 = make_registry(7, use_all_interfaces=True)
    node = make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)
    node.start()
    return node


@pytest.fixture()
def prepared_double_redundant_node():
    registry01 = make_registry(7, use_all_interfaces=True)
    node = make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)
    node.start()
    return node


def get_prepared_double_redundant_node():
    registry01 = make_registry(7, use_all_interfaces=True)
    return make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)
