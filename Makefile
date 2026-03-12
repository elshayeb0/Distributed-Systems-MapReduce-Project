PYTHON := /Users/ZiadElshayeb/Documents/University\ Material/Courses/Distributed\ Systems/.venv/bin/python
PYTEST := PYTHONPATH=. $(PYTHON) -m pytest

.PHONY: test test-base run-t1 run-t1-raw check-t1 clean-output

test:
	$(PYTEST)

test-base:
	$(PYTEST) --cov=src.mapreduce_base --cov-report=term-missing tests/test_mapreduce_base.py

run-t1-raw:
	$(PYTHON) -m src.task1_inverted_index data/raw/T1/*.txt | sort > outputs/InvertedIndex_OUTPUT.txt

run-t1:
	$(PYTHON) -m src.task1_inverted_index data/raw/T1/*.txt | sort | $(PYTHON) -c 'import ast, sys; [print(f"Word: {ast.literal_eval(line.split("\t", 1)[0])}\nDocuments:\n" + "\n".join(f"  - {doc}" for doc in ast.literal_eval(line.split("\t", 1)[1])) + "\n") for line in sys.stdin if line.strip()]' > outputs/InvertedIndex_OUTPUT.txt

check-t1:
	sed -n '1,60p' outputs/InvertedIndex_OUTPUT.txt

clean-output:
	rm -f outputs/InvertedIndex_OUTPUT.txt

coverage:
	$(PYTEST) --cov=src --cov-report=term-missing --cov-report=html