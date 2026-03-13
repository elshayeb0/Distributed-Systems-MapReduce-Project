# Distributed Systems Assignment 1

MapReduce project for GIU Distributed & Web-based Systems.

Implemented tasks:
- Task 1: Inverted Index
- Task 2: Maximum Temperature
- Task 3: Average Movie Rating
- Task 4: Product Sales Total
- Task 5: Most Frequent Word

Project structure:
- `src/`: MRJob task implementations and shared base class
- `tests/`: unit tests for the base class and all tasks
- `data/raw/`: input datasets for Tasks 1 to 5
- `notebooks/`: final Google Colab submission notebook

Useful commands:
- `make test`: run all tests
- `make run-t1` to `make run-t5`: generate task outputs locally
