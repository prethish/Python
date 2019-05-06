.PHONY: test doc-serve test_multithread

NAME = python_general
AUTHORS = Prethish Bhasuran
VERSION = 0.0.0

test_multithread:
	@echo "Temp testing for threading, will be added to tests"
	python tests/___test_multithread.py

test:
	@echo "Running tests"
	python -m unittest discover -s tests -p "test_*" -v

doc-serve:
	python -m mkdocs serve
	@echo "Please open localhost:8000 in the browser."
