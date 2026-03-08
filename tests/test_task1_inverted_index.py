

from __future__ import annotations

from src.task1_inverted_index import MRInvertedIndex


class TestMRInvertedIndex:
    def test_tokenize_normalizes_case_and_strips_punctuation(self) -> None:
        line = "MapReduce, DATA! cloud-processing; analytics."

        tokens = MRInvertedIndex.tokenize(line)

        assert tokens == ["mapreduce", "data", "cloud", "processing", "analytics"]

    def test_tokenize_returns_empty_list_for_non_word_content(self) -> None:
        line = "!!! --- ???"

        tokens = MRInvertedIndex.tokenize(line)

        assert tokens == []

    def test_get_document_name_returns_basename_from_mapreduce_jobconf(self, monkeypatch) -> None:
        def fake_jobconf_from_env(key: str) -> str:
            if key == "mapreduce.map.input.file":
                return "/tmp/input/doc2.txt"
            return ""

        monkeypatch.setattr(
            "src.task1_inverted_index.jobconf_from_env",
            fake_jobconf_from_env,
        )

        assert MRInvertedIndex.get_document_name() == "doc2.txt"

    def test_get_document_name_falls_back_to_legacy_jobconf_key(self, monkeypatch) -> None:
        def fake_jobconf_from_env(key: str) -> str:
            if key == "mapreduce.map.input.file":
                return ""
            if key == "map.input.file":
                return "/var/data/raw/T1/doc3.txt"
            return ""

        monkeypatch.setattr(
            "src.task1_inverted_index.jobconf_from_env",
            fake_jobconf_from_env,
        )

        assert MRInvertedIndex.get_document_name() == "doc3.txt"

    def test_mapper_emits_word_document_pairs_for_each_token(self, monkeypatch) -> None:
        monkeypatch.setattr(MRInvertedIndex, "get_document_name", staticmethod(lambda: "doc1.txt"))
        job = MRInvertedIndex(args=[])

        results = list(job.mapper(None, "Big data and cloud systems"))

        assert results == [
            ("big", "doc1.txt"),
            ("data", "doc1.txt"),
            ("and", "doc1.txt"),
            ("cloud", "doc1.txt"),
            ("systems", "doc1.txt"),
        ]

    def test_mapper_returns_nothing_for_blank_line(self, monkeypatch) -> None:
        monkeypatch.setattr(MRInvertedIndex, "get_document_name", staticmethod(lambda: "doc1.txt"))
        job = MRInvertedIndex(args=[])

        results = list(job.mapper(None, "   \n\t  "))

        assert results == []

    def test_reducer_deduplicates_and_sorts_document_names(self) -> None:
        job = MRInvertedIndex(args=[])

        results = list(job.reducer("analytics", ["doc3.txt", "doc1.txt", "doc3.txt", "doc2.txt"]))

        assert results == [
            ("analytics", ["doc1.txt", "doc2.txt", "doc3.txt"]),
        ]