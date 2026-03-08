"""Base MRJob template for the Distributed Systems MapReduce project.

Task-specific jobs should inherit from ``BaseMapReduceJob`` and implement the
``mapper`` and ``reducer`` methods.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from mrjob.job import MRJob


class BaseMapReduceJob(MRJob):
    """Shared base class for all project MapReduce jobs."""

    @staticmethod
    def clean_line(line: str) -> str:
        """Return a normalized input line with surrounding whitespace removed."""
        return line.strip()

    @staticmethod
    def is_blank(line: str) -> bool:
        """Return ``True`` when the provided line is empty after normalization."""
        return not line.strip()

    def mapper(self, _: Any, line: str) -> Iterable[tuple[Any, Any]]:
        """Map input records to intermediate key-value pairs.

        Subclasses must override this method.
        """
        raise NotImplementedError("Subclasses must implement mapper().")

    def reducer(self, key: Any, values: Iterable[Any]) -> Iterable[tuple[Any, Any]]:
        """Reduce grouped values into final key-value output.

        Subclasses must override this method.
        """
        raise NotImplementedError("Subclasses must implement reducer().")


if __name__ == "__main__":
    BaseMapReduceJob.run()