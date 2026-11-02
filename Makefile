test:
	pytest

unit_test:
	pytest -m "not performance"

perf_test:
	pytest -m performance

coverage:
	coverage run -m pytest && coverage report --show-missing --fail-under=90

lint:
	ruff check

doc:
	pdoc --html --output-dir docs --force .
