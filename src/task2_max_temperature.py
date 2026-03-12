from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from src.mapreduce_base import BaseMapReduceJob


class MRMaxTemperature(BaseMapReduceJob):
    """Find the maximum temperature for each year."""

    @staticmethod
    def parse_line(line: str) -> tuple[str, float]:
        """Parse a line in the form YYYY-MM-DD,temperature."""
        date_str, temperature_str = line.split(",", 1)
        year = date_str[:4]
        temperature = float(temperature_str)
        return year, temperature

    def mapper(self, _: Any, line: str) -> Iterable[tuple[str, float]]:
        """Emit (year, temperature) for each valid reading."""
        cleaned_line = self.clean_line(line)
        if self.is_blank(cleaned_line):
            return

        year, temperature = self.parse_line(cleaned_line)
        yield year, temperature

    def reducer(self, key: str, values: Iterable[float]) -> Iterable[tuple[str, float]]:
        """Emit (year, max_temperature)."""
        yield key, max(values)


if __name__ == "__main__":
    MRMaxTemperature.run()