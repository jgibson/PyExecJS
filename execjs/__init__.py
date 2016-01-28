#!/usr/bin/env python3
# -*- coding: ascii -*-
from __future__ import unicode_literals, division, with_statement
'''
    Run JavaScript code from Python.

    PyExecJS is a porting of ExecJS from Ruby.
    PyExecJS automatically picks the best runtime available to evaluate your JavaScript program,
    then returns the result to you as a Python object.

    A short example:

>>> import execjs
>>> execjs.eval("'red yellow blue'.split(' ')")
['red', 'yellow', 'blue']
>>> ctx = execjs.compile("""
...     function add(x, y) {
...         return x + y;
...     }
... """)
>>> ctx.call("add", 1, 2)
3
'''

import os
import os.path

import execjs.pyv8runtime as pyv8runtime
import execjs.external_runtime as external_runtime
ExternalRuntime = external_runtime.ExternalRuntime

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

__all__ = """
    get register runtimes get_from_environment exec_ eval compile
    ExternalRuntime Context
    Error RuntimeError ProgramError RuntimeUnavailable
""".split()


class Error(Exception):
    pass


class RuntimeError(Error):
    pass


class ProgramError(Error):
    pass


class RuntimeUnavailable(RuntimeError):
    pass


def register(name, runtime):
    '''Register a JavaScript runtime.'''
    _runtimes[name] = runtime


def get(name=None):
    """
    Return a appropriate JavaScript runtime.
    If name is specified, return the runtime.
    """
    if name is None:
        return _auto_detect()

    try:
        runtime = runtimes()[name]
    except KeyError:
        raise RuntimeUnavailable("{name} runtime is not defined".format(name=name))
    else:
        if not runtime.is_available():
            raise RuntimeUnavailable(
                "{name} runtime is not available on this system".format(name=runtime.name))
        return runtime


def runtimes():
    """return a dictionary of all supported JavaScript runtimes."""
    return dict(_runtimes)


def available_runtimes():
    """return a dictionary of all supported JavaScript runtimes which is usable"""
    return dict((name, runtime) for name, runtime in _runtimes.items() if runtime.is_available())


def _auto_detect():
    runtime = get_from_environment()
    if runtime is not None:
        return runtime

    for runtime in _runtimes.values():
        if runtime.is_available():
            return runtime

    raise RuntimeUnavailable("Could not find a JavaScript runtime.")


def get_from_environment():
    '''
        Return the JavaScript runtime that is specified in EXECJS_RUNTIME environment variable.
        If EXECJS_RUNTIME environment variable is empty or invalid, return None.
    '''
    try:
        name = os.environ["EXECJS_RUNTIME"]
    except KeyError:
        return None

    if not name:
        return None
    return get(name)


def eval(source):
    return get().eval(source)


def exec_(source):
    return get().exec_(source)


def compile(source):
    return get().compile(source)


_runtimes = OrderedDict()
register('PyV8', pyv8runtime.PyV8Runtime())
register('PyQt5', pyv8runtime.PyV8Runtime())

if external_runtime.node.is_available():
    register("Node", external_runtime.node)
else:
    register("Node", external_runtime.nodejs)

register('JavaScriptCore', external_runtime.jsc)
register('SpiderMonkey', external_runtime.spidermonkey)
register('Spidermonkey', external_runtime.spidermonkey)
register('JScript', external_runtime.jscript)
register("PhantomJS", external_runtime.phantomjs)
register("SlimerJS", external_runtime.slimerjs)
