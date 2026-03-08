from src.mapreduce_base import BaseMapReduceJob


def test_clean_line_strips_whitespace():
    assert BaseMapReduceJob.clean_line("  hello world  \n") == "hello world"


def test_is_blank_with_empty_string():
    assert BaseMapReduceJob.is_blank("") is True


def test_is_blank_with_whitespace_only():
    assert BaseMapReduceJob.is_blank("   \n\t  ") is True


def test_is_blank_with_content():
    assert BaseMapReduceJob.is_blank("data") is False


def test_mapper_raises_not_implemented():
    job = BaseMapReduceJob(args=[])
    try:
        list(job.mapper(None, "sample line"))
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        assert True


def test_reducer_raises_not_implemented():
    job = BaseMapReduceJob(args=[])
    try:
        list(job.reducer("key", ["value1", "value2"]))
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        assert True