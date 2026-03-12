from __future__ import annotations

from src.task5_most_frequent_word import MRMostFrequentWord


class TestMRMostFrequentWord:
    def test_tokenize_normalizes_case(self) -> None:
        tokens = MRMostFrequentWord.tokenize("Big DATA systems")

        assert tokens == ["big", "data", "systems"]

    def test_mapper_emits_word_counts(self) -> None:
        job = MRMostFrequentWord(args=[])

        results = list(job.mapper(None, "big data systems"))

        assert results == [("big", 1), ("data", 1), ("systems", 1)]

    def test_mapper_skips_blank_line(self) -> None:
        job = MRMostFrequentWord(args=[])

        results = list(job.mapper(None, "   \n\t  "))

        assert results == []

    def test_reducer_sums_word_counts(self) -> None:
        job = MRMostFrequentWord(args=[])

        results = list(job.reducer("data", [1, 1, 1, 1, 1]))

        assert results == [("data", 5)]

    def test_mapper_find_max_emits_common_key(self) -> None:
        job = MRMostFrequentWord(args=[])

        results = list(job.mapper_find_max("data", 7))

        assert results == [("most_frequent", ("data", 7))]

    def test_reducer_find_max_returns_highest_frequency(self) -> None:
        job = MRMostFrequentWord(args=[])

        results = list(
            job.reducer_find_max(
                "most_frequent",
                [("big", 4), ("data", 9), ("systems", 6)],
            )
        )

        assert results == [("data", 9)]

    def test_reducer_find_max_breaks_ties_lexicographically(self) -> None:
        job = MRMostFrequentWord(args=[])

        results = list(
            job.reducer_find_max(
                "most_frequent",
                [("systems", 8), ("data", 8)],
            )
        )

        assert results == [("data", 8)]

    def test_steps_returns_one_step_for_intermediate_only_mode(self) -> None:
        job = MRMostFrequentWord(args=["--intermediate-only"])

        steps = job.steps()

        assert len(steps) == 1

    def test_steps_returns_two_steps_for_full_mode(self) -> None:
        job = MRMostFrequentWord(args=[])

        steps = job.steps()

        assert len(steps) == 2