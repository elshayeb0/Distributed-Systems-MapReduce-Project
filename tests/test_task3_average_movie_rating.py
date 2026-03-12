from __future__ import annotations

from src.task3_average_movie_rating import MRAverageMovieRating


class TestMRAverageMovieRating:
    def test_parse_line_extracts_movie_id_and_rating(self) -> None:
        movie_id, rating = MRAverageMovieRating.parse_line("1,101,4")

        assert movie_id == "101"
        assert rating == 4.0

    def test_compute_average_uses_sum_and_count(self) -> None:
        average = MRAverageMovieRating.compute_average([4.0, 5.0, 3.0, 4.0, 5.0])

        assert average == 4.2

    def test_mapper_emits_movie_id_and_rating(self) -> None:
        job = MRAverageMovieRating(args=[])

        results = list(job.mapper(None, "2,105,5"))

        assert results == [("105", 5.0)]

    def test_mapper_skips_header_row(self) -> None:
        job = MRAverageMovieRating(args=[])

        results = list(job.mapper(None, "user_id,movie_id,rating"))

        assert results == []

    def test_mapper_returns_nothing_for_blank_line(self) -> None:
        job = MRAverageMovieRating(args=[])

        results = list(job.mapper(None, "   \n\t  "))

        assert results == []

    def test_reducer_returns_average_rating_for_movie(self) -> None:
        job = MRAverageMovieRating(args=[])

        results = list(job.reducer("101", [4.0, 5.0, 3.0, 4.0, 5.0]))

        assert results == [("101", 4.2)]