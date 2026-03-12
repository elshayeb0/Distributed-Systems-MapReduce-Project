from __future__ import annotations

import re
from collections.abc import Iterable, Iterator
from typing import Any

from mrjob.step import MRStep

from src.mapreduce_base import BaseMapReduceJob


class MRMostFrequentWord(BaseMapReduceJob):
    """Find the most frequent word in a text document."""

    WORD_PATTERN = re.compile(r"\b[a-zA-Z0-9]+\b")

    def configure_args(self) -> None:
        """Add a flag to stop after the intermediate word-count step."""
        super().configure_args()
        self.add_passthru_arg(
            "--intermediate-only",
            action="store_true",
            help="Run only the word-frequency step and output intermediate counts.",
        )

    @classmethod
    def tokenize(cls, line: str) -> list[str]:
        """Normalize and tokenize a line into lowercase words."""
        return cls.WORD_PATTERN.findall(line.lower())

    def mapper(self, _: Any, line: str) -> Iterable[tuple[str, int]]:
        """Emit (word, 1) for each token."""
        cleaned_line = self.clean_line(line)
        if self.is_blank(cleaned_line):
            return

        for word in self.tokenize(cleaned_line):
            yield word, 1

    def reducer(self, key: str, values: Iterable[int]) -> Iterable[tuple[str, int]]:
        """Emit (word, total_count)."""
        yield key, sum(values)

    def mapper_find_max(self, word: str, frequency: int) -> Iterator[tuple[str, tuple[str, int]]]:
        """Send all word counts to one reducer for global max selection."""
        yield "most_frequent", (word, frequency)

    def reducer_find_max(
        self, _: str, values: Iterable[tuple[str, int]]
    ) -> Iterator[tuple[str, int]]:
        """Emit (most_frequent_word, frequency)."""
        most_frequent_word = ""
        max_frequency = -1

        for word, frequency in values:
            if frequency > max_frequency:
                most_frequent_word = word
                max_frequency = frequency
            elif frequency == max_frequency and word < most_frequent_word:
                most_frequent_word = word

        yield most_frequent_word, max_frequency

    def steps(self) -> list[MRStep]:
        """Run either the intermediate word-count step or the full two-step pipeline."""
        word_count_step = MRStep(mapper=self.mapper, reducer=self.reducer)

        if self.options.intermediate_only:
            return [word_count_step]

        return [
            word_count_step,
            MRStep(mapper=self.mapper_find_max, reducer=self.reducer_find_max),
        ]


if __name__ == "__main__":
    MRMostFrequentWord.run()