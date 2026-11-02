test:
	pytest

unit_test:
	pytest -m "not performance"

perf_test:
	pytest -m performance
