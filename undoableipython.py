#!/usr/bin/env python

"""
undoableipython

This module contains a replacement for the
TerminalInteractiveShell.raw_input_original method that can be found in
IPython source code. The replacement implements undoable feature for ipython
without rewriting the terminal (you will see the history of written statements
but the last statement will be undone).

Use it from the command line: `python undoableipython.py`
"""

from __future__ import unicode_literals
import os
import sys
from IPython.utils import py3compat
from IPython.terminal.interactiveshell import TerminalInteractiveShell
from IPython import start_ipython


def raw_input_original(prompt):
    """Replace raw_input_original property in TerminalInteractiveShell.

    Add code to implement undo feature in IPython terminal. The original
    IPython code is wrapped into comments, the rest is part of the hack.

    Args:
        prompt (str): Prompt input from the user.

    Returns:
        str: The input from the user processed.
    """

    from functools import partial
    import socket

    if sys.version_info.major == 2:
        ConnectionRefusedError = socket.error

    def connect_and_wait_for_close(port):
        s = socket.socket()
        try:
            s.connect(('localhost', port))
        except ConnectionRefusedError:
            pass
        else:
            assert b'' == s.recv(1024)

    save = partial(connect_and_wait_for_close, port=4242)
    restore = partial(connect_and_wait_for_close, port=4243)

    while True:
        save()
        try:
            # **********************************************
            # --------BEGIN of Original IPython code--------
            # **********************************************
            if py3compat.PY3:
                line = input(prompt)
            else:
                line = raw_input(prompt)
            # **********************************************
            # --------END of Original IPython code--------
            # **********************************************
        except KeyboardInterrupt:
            line = "undo"

        if line == "undo":
            restore()
            os._exit(42)

        pid = os.fork()
        is_child = pid == 0

        # if the process is not the parent, just carry on
        if is_child:
            break

        else:
            while True:
                try:
                    status = os.waitpid(pid, 0)
                    break
                except KeyboardInterrupt:
                    pass
            exit_code = status[1] // 256
            if not exit_code == 42:
                os._exit(exit_code)

    return line


def patch_ipython():
    """Replace raw_input_original as a property."""
    TerminalInteractiveShell.raw_input_original = property(
        lambda self: raw_input_original, lambda self, x: None)


def rl_is_ipython(rl_path):
    """Check if the terminal to be opened is ipython.

    Args:
        rl_path (str): Path of interpreter being called.
    """
    return os.path.basename(rl_path) == "ipython"


def start_undoable_ipython(args=None):
    """Start an undoable instance of ipython.

    Args:
        args (list): Arguments passed to the undoable instance to be started.
    """
    patch_ipython()

    if args:
        sys.argv = args

    start_ipython()


if __name__ == '__main__':
    start_undoable_ipython()
