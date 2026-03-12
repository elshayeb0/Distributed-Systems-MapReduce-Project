PYTHON := /Users/ZiadElshayeb/Documents/University\ Material/Courses/Distributed\ Systems/.venv/bin/python
PYTEST := PYTHONPATH=. $(PYTHON) -m pytest

.PHONY: test test-base test-t3 test-t4 run-t1 run-t1-raw check-t1 run-t2 check-t2 run-t3 check-t3 run-t4 check-t4 clean-output coverage coverage-t3 coverage-t4 test-t5 run-t5 check-t5 coverage-t5

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

run-t2:
	$(PYTHON) -m src.task2_max_temperature data/raw/T2/temperature_readings.txt | sort > outputs/MaximumTemperature_OUTPUT.txt

check-t2:
	sed -n '1,60p' outputs/MaximumTemperature_OUTPUT.txt

run-t3:
	$(PYTHON) -m src.task3_average_movie_rating data/raw/T3/movie_ratings.txt | sort > outputs/AverageMovieRating_OUTPUT.txt

check-t3:
	sed -n '1,60p' outputs/AverageMovieRating_OUTPUT.txt

run-t4:
	$(PYTHON) -m src.task4_product_sales_total data/raw/T4/product_sales.txt | sort > outputs/ProductSalesTotal_OUTPUT.txt

check-t4:
	sed -n '1,60p' outputs/ProductSalesTotal_OUTPUT.txt

test-t3:
	$(PYTEST) --cov=src.task3_average_movie_rating --cov-report=term-missing tests/test_task3_average_movie_rating.py

test-t4:
	$(PYTEST) --cov=src.task4_product_sales_total --cov-report=term-missing tests/test_task4_product_sales_total.py

coverage-t3:
	$(PYTEST) --cov=src.task3_average_movie_rating --cov-report=term-missing --cov-report=html tests/test_task3_average_movie_rating.py

coverage-t4:
	$(PYTEST) --cov=src.task4_product_sales_total --cov-report=term-missing --cov-report=html tests/test_task4_product_sales_total.py

run-t5:
	$(PYTHON) -m src.task5_most_frequent_word data/raw/T5/bonus_text.txt > outputs/MostFrequentWord_OUTPUT.txt

check-t5:
	sed -n '1,60p' outputs/MostFrequentWord_OUTPUT.txt

test-t5:
	$(PYTEST) --cov=src.task5_most_frequent_word --cov-report=term-missing tests/test_task5_most_frequent_word.py

coverage-t5:
	$(PYTEST) --cov=src.task5_most_frequent_word --cov-report=term-missing --cov-report=html tests/test_task5_most_frequent_word.py

clean-output:
	rm -f outputs/InvertedIndex_OUTPUT.txt outputs/MaximumTemperature_OUTPUT.txt outputs/AverageMovieRating_OUTPUT.txt outputs/ProductSalesTotal_OUTPUT.txt outputs/MostFrequentWord_OUTPUT.txt

coverage:
	$(PYTEST) --cov=src --cov-report=term-missing --cov-report=html