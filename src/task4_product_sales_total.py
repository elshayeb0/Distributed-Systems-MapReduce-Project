from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from src.mapreduce_base import BaseMapReduceJob


class MRProductSalesTotal(BaseMapReduceJob):
    """Compute total sales for each product."""

    @staticmethod
    def parse_line(line: str) -> tuple[str, float]:
        """Extract product_id and amount from a CSV row."""
        _transaction_id, product_id, amount = line.split(",", 2)
        return product_id, float(amount)

    @staticmethod
    def compute_total(values: Iterable[float]) -> float:
        """Sum all sales values."""
        total = 0.0
        for value in values:
            total += value
        return round(total, 2)

    def mapper(self, _: Any, line: str) -> Iterable[tuple[str, float]]:
        """Emit (product_id, amount) for each valid sales row."""
        cleaned_line = self.clean_line(line)

        if self.is_blank(cleaned_line):
            return

        if cleaned_line.startswith("transaction_id"):
            return

        product_id, amount = self.parse_line(cleaned_line)
        yield product_id, amount

    def reducer(self, key: str, values: Iterable[float]) -> Iterable[tuple[str, float]]:
        """Emit (product_id, total_sales)."""
        yield key, self.compute_total(values)


if __name__ == "__main__":
    MRProductSalesTotal.run()