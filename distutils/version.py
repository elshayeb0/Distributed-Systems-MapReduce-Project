"""Compatibility shim for distutils.version."""

from packaging.version import Version


class LooseVersion:
    """Small compatibility wrapper around packaging.version.Version."""

    def __init__(self, version):
        self.vstring = str(version)
        self._version = Version(self.vstring)

    def __repr__(self):
        return f"LooseVersion ('{self.vstring}')"

    def __str__(self):
        return self.vstring

    def _coerce_other(self, other):
        if isinstance(other, LooseVersion):
            return other._version
        return Version(str(other))

    def __eq__(self, other):
        return self._version == self._coerce_other(other)

    def __lt__(self, other):
        return self._version < self._coerce_other(other)

    def __le__(self, other):
        return self._version <= self._coerce_other(other)

    def __gt__(self, other):
        return self._version > self._coerce_other(other)

    def __ge__(self, other):
        return self._version >= self._coerce_other(other)

    def __ne__(self, other):
        return self._version != self._coerce_other(other)