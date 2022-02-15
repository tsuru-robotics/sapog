#
# Copyright (c) 2022 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
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


# If you want to import this in something other than tests, then add_deps is a function that can be imported.
def add_deps():
    """This is necessary to extend the python path with the compiled DSDL."""
    source_path = pathlib.Path(__file__).parent.absolute()
    dependency_path = source_path.parent / "deps"
    namespace_path = dependency_path / "namespaces"
    print(f"Namespace path: {namespace_path.absolute()}")
    sys.path.insert(0, str(namespace_path.absolute()))

# def pytest_runtest_makereport(item, call):
#     print("\n\n\n\nMaking a report\n\n\n\n")
#     from _pytest.runner import pytest_runtest_makereport as orig_pytest_runtest_makereport
#     tr = orig_pytest_runtest_makereport(item, call)
#
#     if call.excinfo is not None:
#         if call.excinfo.errisinstance(RuntimeError) or call.excinfo.errisinstance(ImportError):
#             tr.outcome = 'skipped'
#             tr.wasxfail = "reason: SomeExceptionFromLibrary. shame on them..."
#
#     return tr

# @pytest.hookimpl(trylast=True)
# def pytest_configure(config):
#     print("\n\n\nPytest configuration hook\n\n\n")
#     # unregister returns the unregistered plugin
#     pdbinvoke = config.pluginmanager.unregister(name="pdbinvoke")
#     if pdbinvoke is None:
#         # no --pdb switch used, no debugging requested
#         return
#     print("Configuring ExceptionFilter")
#     # get the terminalreporter too, to write to the console
#     tr = config.pluginmanager.getplugin("terminalreporter")
#     # create or own plugin
#     plugin = ExceptionFilter(pdbinvoke, tr)
#
#     # register our plugin, pytest will then start calling our plugin hooks
#     config.pluginmanager.register(plugin, "exception_filter")
#
#
# class ExceptionFilter:
#     def __init__(self, terminalreporter):
#         # provide the same functionality as pdbinvoke
#         self.orig_exception_interact = pdbinvoke.pytest_exception_interact
#         self.tr = terminalreporter
#
#     def pytest_exception_interact(self, node, call, report):
#         if call.excinfo.errisinstance(RuntimeError) or call.excinfo.errisinstance(ImportError):
#             self.tr.write_line("Not interested in RuntimeErrors or ImportErrors!")
#             return
#         return self.orig_exception_interact(node, call, report)
