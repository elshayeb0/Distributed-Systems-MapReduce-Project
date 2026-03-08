"""
Compatibility shim for the removed Python `pipes` module.

Python removed the `pipes` module in Python 3.13+.
Older libraries like `mrjob` still import `pipes.quote`.
This file restores that function using `shlex.quote`.
"""

from shlex import quote

__all__ = ["quote"]