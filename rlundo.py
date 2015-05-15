#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
rlundo

Start a repl with undo feature.
"""

from __future__ import unicode_literals
import sys

from rlundoable import modify_env_with_modified_rl
from rewrite import run_with_listeners
import undoablepython
import undoableipython


def start_undoable_rl(args):
    """Start an undoable repl.

    Python and IPython repls have specific modules to patch the method used to
    catch user input. For the rest, C readline method is replaced with a
    modified version.

    Args:
        args (list): Arguments passed to rlundo.py
    """

    if undoablepython.rl_is_python(args[1]):
        commands = ["python", "undoablepython.py"] + args[2:]
        run_with_listeners(commands)

    elif undoableipython.rl_is_ipython(args[1]):
        commands = ["python", "undoableipython.py"] + args[2:]
        run_with_listeners(commands)

    else:
        modify_env_with_modified_rl()
        run_with_listeners(args[1:])


if __name__ == "__main__":
    start_undoable_rl(sys.argv)
