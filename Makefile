# ============================================================
# Distributed Systems Project 1 - Task Runner
# ============================================================

# ============================================================
# Python / Pytest configuration
# ============================================================
PYTHON ?= python3
PYTEST := PYTHONPATH=. $(PYTHON) -m pytest
CHECK_LINES := 60
OUTPUT_DIR := outputs

# ============================================================
# Output files
# ============================================================
T1_OUTPUT := $(OUTPUT_DIR)/InvertedIndex_OUTPUT.txt
T2_OUTPUT := $(OUTPUT_DIR)/MaximumTemperature_OUTPUT.txt
T3_OUTPUT := $(OUTPUT_DIR)/AverageMovieRating_OUTPUT.txt
T4_OUTPUT := $(OUTPUT_DIR)/ProductSalesTotal_OUTPUT.txt
T5_INTERMEDIATE_OUTPUT := $(OUTPUT_DIR)/WordFrequency_OUTPUT.txt
T5_OUTPUT := $(OUTPUT_DIR)/MostFrequentWord_OUTPUT.txt

# ============================================================
# Phony targets
# ============================================================
.PHONY: \
	test test-base coverage clean-output \
	run-t1-raw run-t1 check-t1 test-t1 coverage-t1 \
	run-t2 check-t2 test-t2 coverage-t2 \
	run-t3 check-t3 test-t3 coverage-t3 \
	run-t4 check-t4 test-t4 coverage-t4 \
	run-t5-intermediate check-t5-intermediate \
	run-t5 check-t5 test-t5 coverage-t5

$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

# ============================================================
# General project targets
# ============================================================
test:
	$(PYTEST)

test-base:
	$(PYTEST) --cov=src.mapreduce_base --cov-report=term-missing tests/test_mapreduce_base.py

coverage:
	$(PYTEST) --cov=src --cov-report=term-missing --cov-report=html

clean-output:
	rm -f $(T1_OUTPUT) $(T2_OUTPUT) $(T3_OUTPUT) $(T4_OUTPUT) $(T5_INTERMEDIATE_OUTPUT) $(T5_OUTPUT)

# ============================================================
# Task 1 - Inverted Index
# ============================================================
run-t1-raw: $(OUTPUT_DIR)
	$(PYTHON) -m src.task1_inverted_index data/raw/T1/*.txt | sort > $(T1_OUTPUT)

run-t1: $(OUTPUT_DIR)
	$(PYTHON) -m src.task1_inverted_index data/raw/T1/*.txt | sort | $(PYTHON) -c 'import ast, sys; [print(f"Word: {ast.literal_eval(line.split("\t", 1)[0])}\nDocuments:\n" + "\n".join(f"  - {doc}" for doc in ast.literal_eval(line.split("\t", 1)[1])) + "\n") for line in sys.stdin if line.strip()]' > $(T1_OUTPUT)

check-t1:
	sed -n '1,$(CHECK_LINES)p' $(T1_OUTPUT)

test-t1:
	$(PYTEST) --cov=src.task1_inverted_index --cov-report=term-missing tests/test_task1_inverted_index.py

coverage-t1:
	$(PYTEST) --cov=src.task1_inverted_index --cov-report=term-missing --cov-report=html tests/test_task1_inverted_index.py

# ============================================================
# Task 2 - Maximum Temperature
# ============================================================
run-t2: $(OUTPUT_DIR)
	$(PYTHON) -m src.task2_max_temperature data/raw/T2/temperature_readings.txt | sort > $(T2_OUTPUT)

check-t2:
	sed -n '1,$(CHECK_LINES)p' $(T2_OUTPUT)

test-t2:
	$(PYTEST) --cov=src.task2_max_temperature --cov-report=term-missing tests/test_task2_max_temperature.py

coverage-t2:
	$(PYTEST) --cov=src.task2_max_temperature --cov-report=term-missing --cov-report=html tests/test_task2_max_temperature.py

# ============================================================
# Task 3 - Average Movie Rating
# ============================================================
run-t3: $(OUTPUT_DIR)
	$(PYTHON) -m src.task3_average_movie_rating data/raw/T3/movie_ratings.txt | sort > $(T3_OUTPUT)

check-t3:
	sed -n '1,$(CHECK_LINES)p' $(T3_OUTPUT)

test-t3:
	$(PYTEST) --cov=src.task3_average_movie_rating --cov-report=term-missing tests/test_task3_average_movie_rating.py

coverage-t3:
	$(PYTEST) --cov=src.task3_average_movie_rating --cov-report=term-missing --cov-report=html tests/test_task3_average_movie_rating.py

# ============================================================
# Task 4 - Product Sales Total
# ============================================================
run-t4: $(OUTPUT_DIR)
	$(PYTHON) -m src.task4_product_sales_total data/raw/T4/product_sales.txt | sort > $(T4_OUTPUT)

check-t4:
	sed -n '1,$(CHECK_LINES)p' $(T4_OUTPUT)

test-t4:
	$(PYTEST) --cov=src.task4_product_sales_total --cov-report=term-missing tests/test_task4_product_sales_total.py

coverage-t4:
	$(PYTEST) --cov=src.task4_product_sales_total --cov-report=term-missing --cov-report=html tests/test_task4_product_sales_total.py

# ============================================================
# Task 5 - Most Frequent Word
# ============================================================
run-t5-intermediate: $(OUTPUT_DIR)
	$(PYTHON) -m src.task5_most_frequent_word --intermediate-only data/raw/T5/bonus_text.txt | sort > $(T5_INTERMEDIATE_OUTPUT)

check-t5-intermediate:
	sed -n '1,$(CHECK_LINES)p' $(T5_INTERMEDIATE_OUTPUT)

run-t5: $(OUTPUT_DIR)
	$(PYTHON) -m src.task5_most_frequent_word data/raw/T5/bonus_text.txt > $(T5_OUTPUT)

check-t5:
	sed -n '1,$(CHECK_LINES)p' $(T5_OUTPUT)

test-t5:
	$(PYTEST) --cov=src.task5_most_frequent_word --cov-report=term-missing tests/test_task5_most_frequent_word.py

coverage-t5:
	$(PYTEST) --cov=src.task5_most_frequent_word --cov-report=term-missing --cov-report=html tests/test_task5_most_frequent_word.py
