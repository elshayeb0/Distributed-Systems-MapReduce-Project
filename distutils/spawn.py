"""Compatibility shim for distutils.spawn."""

from shutil import which


def find_executable(executable, path=None):
    """Return the path to an executable or None if not found."""
    return which(executable, path=path)