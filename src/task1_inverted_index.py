from __future__ import annotations

import os
import re
from collections.abc import Iterable
from typing import Any

from mrjob.compat import jobconf_from_env

from src.mapreduce_base import BaseMapReduceJob


class MRInvertedIndex(BaseMapReduceJob):
    """Build an inverted index from multiple text documents."""

    JOBCONF = {"mapreduce.job.reduces": "1"}
    WORD_PATTERN = re.compile(r"\b[a-zA-Z0-9]+\b")

    @staticmethod
    def get_document_name() -> str:
        """Return the current input document name."""
        input_path = (
            jobconf_from_env("mapreduce.map.input.file")
            or jobconf_from_env("map.input.file")
            or ""
        )
        return os.path.basename(input_path)

    @classmethod
    def tokenize(cls, line: str) -> list[str]:
        """Normalize and tokenize a line into lowercase words."""
        return cls.WORD_PATTERN.findall(line.lower())

    def mapper(self, _: Any, line: str) -> Iterable[tuple[str, str]]:
        """Emit (word, document_name) for each word in the current document."""
        cleaned_line = self.clean_line(line)
        if self.is_blank(cleaned_line):
            return

        document_name = self.get_document_name()
        for word in self.tokenize(cleaned_line):
            yield word, document_name

    def reducer(self, key: str, values: Iterable[str]) -> Iterable[tuple[str, list[str]]]:
        """Emit each word once with a sorted unique list of document names."""
        unique_documents = sorted(set(values))
        yield key, unique_documents


if __name__ == "__main__":
    MRInvertedIndex.run()