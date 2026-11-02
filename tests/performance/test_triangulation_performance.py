"""Performance tests for the triangulation algorithm."""

import random
import statistics
import time

import pytest
from triangulation import triangulate

NUMBER_OF_RUNS = 5

PERFORMANCE_LIMITS = {
    100: 1.00,
    500: 5.00,
    1000: 15.00,
}


def generate_points(number_of_points):
    """Generate reproducible, non-duplicated random points."""
    generator = random.Random(42)
    points = set()

    while len(points) < number_of_points:
        x = generator.uniform(-1000, 1000)
        y = generator.uniform(-1000, 1000)
        points.add((x, y))

    return list(points)


def measure_median(function, number_of_runs=NUMBER_OF_RUNS):
    """Measure a function several times and return its median duration."""
    durations = []

    for _ in range(number_of_runs):
        start = time.perf_counter()
        function()
        durations.append(time.perf_counter() - start)

    return statistics.median(durations)


@pytest.mark.performance
@pytest.mark.parametrize(
    ("number_of_points", "maximum_time"),
    PERFORMANCE_LIMITS.items(),
)
def test_triangulation_performance(number_of_points, maximum_time):
    """Ensure triangulation stays below its size-specific threshold."""
    points = generate_points(number_of_points)

    median_time = measure_median(
        lambda: triangulate(points),
    )

    assert median_time < maximum_time, (
        f"Triangulation of {number_of_points} points took "
        f"{median_time:.4f}s; maximum allowed is {maximum_time}s"
    )