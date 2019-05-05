.PHONY: test doc-serve

NAME = python_general
AUTHORS = Prethish Bhasuran
VERSION = 0.0.0

clean:
	@echo "Cleaning"

test:
	@echo "Running tests"
	python -m unittest discover -s tests -p "test_*" -v

doc-serve:
	python -m mkdocs serve
	@echo "Please open localhost:8000 in the browser."
