from __future__ import annotations

from src.task2_max_temperature import MRMaxTemperature


class TestMRMaxTemperature:
    def test_parse_line_extracts_year_and_temperature(self) -> None:
        year, temperature = MRMaxTemperature.parse_line("2002-06-30,40.5")

        assert year == "2002"
        assert temperature == 40.5

    def test_mapper_emits_year_temperature_pair(self) -> None:
        job = MRMaxTemperature(args=[])

        results = list(job.mapper(None, "2001-07-25,39.1"))

        assert results == [("2001", 39.1)]

    def test_mapper_returns_nothing_for_blank_line(self) -> None:
        job = MRMaxTemperature(args=[])

        results = list(job.mapper(None, "   \n\t  "))

        assert results == []

    def test_reducer_returns_max_temperature_for_year(self) -> None:
        job = MRMaxTemperature(args=[])

        results = list(job.reducer("2000", [18.5, 25.0, 37.8, 35.4, 22.1]))

        assert results == [("2000", 37.8)]