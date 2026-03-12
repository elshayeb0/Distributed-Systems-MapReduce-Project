from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from src.mapreduce_base import BaseMapReduceJob


class MRAverageMovieRating(BaseMapReduceJob):
    """Compute the average rating for each movie."""

    @staticmethod
    def parse_line(line: str) -> tuple[str, float]:
        """Extract movie_id and rating from a CSV row."""
        _user_id, movie_id, rating = line.split(",", 2)
        return movie_id, float(rating)

    @staticmethod
    def compute_average(values: Iterable[float]) -> float:
        """Compute an average from an iterable of ratings using sum and count."""
        total = 0.0
        count = 0

        for value in values:
            total += value
            count += 1

        return round(total / count, 2)

    def mapper(self, _: Any, line: str) -> Iterable[tuple[str, float]]:
        """Emit (movie_id, rating) for each valid rating row."""
        cleaned_line = self.clean_line(line)

        if self.is_blank(cleaned_line):
            return

        if cleaned_line.startswith("user_id"):
            return

        movie_id, rating = self.parse_line(cleaned_line)
        yield movie_id, rating

    def reducer(self, key: str, values: Iterable[float]) -> Iterable[tuple[str, float]]:
        """Emit (movie_id, average_rating)."""
        yield key, self.compute_average(values)


if __name__ == "__main__":
    MRAverageMovieRating.run()