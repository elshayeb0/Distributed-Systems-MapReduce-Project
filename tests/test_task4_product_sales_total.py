from __future__ import annotations

from src.task4_product_sales_total import MRProductSalesTotal


class TestMRProductSalesTotal:
    def test_parse_line_extracts_product_and_amount(self) -> None:
        product_id, amount = MRProductSalesTotal.parse_line("1,P101,120.5")

        assert product_id == "P101"
        assert amount == 120.5

    def test_compute_total_sums_values(self) -> None:
        total = MRProductSalesTotal.compute_total([120.5, 50.0, 130.0, 80.0])

        assert total == 380.5

    def test_mapper_emits_product_and_amount(self) -> None:
        job = MRProductSalesTotal(args=[])

        results = list(job.mapper(None, "1,P101,120.5"))

        assert results == [("P101", 120.5)]

    def test_mapper_skips_header(self) -> None:
        job = MRProductSalesTotal(args=[])

        results = list(job.mapper(None, "transaction_id,product_id,amount"))

        assert results == []

    def test_mapper_skips_blank_line(self) -> None:
        job = MRProductSalesTotal(args=[])

        results = list(job.mapper(None, "   \n"))

        assert results == []

    def test_reducer_returns_total_sales(self) -> None:
        job = MRProductSalesTotal(args=[])

        results = list(job.reducer("P101", [120.5, 50.0, 130.0, 80.0]))

        assert results == [("P101", 380.5)]