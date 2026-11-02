"""Performance tests for binary PointSet and Triangles operations."""

import statistics
import time

import pytest
from decoder import decode_point_set
from encoder import encode_point_set, encode_triangle_set

NUMBER_OF_RUNS = 5
MAX_DECODE_TIME = 0.10
MAX_ENCODE_TIME = 0.10


def measure_median(function, number_of_runs=NUMBER_OF_RUNS):
    """Measure a function several times and return its median duration."""
    durations = []

    for _ in range(number_of_runs):
        start = time.perf_counter()
        function()
        durations.append(time.perf_counter() - start)

    return statistics.median(durations)


def generate_points(number_of_points):
    """Generate a reproducible set of points."""
    return [
        (float(index), float(index * 2))
        for index in range(number_of_points)
    ]


def generate_triangles(number_of_vertices, number_of_triangles):
    """Generate triangles whose indices refer to existing vertices."""
    return [
        (
            index % number_of_vertices,
            (index + 1) % number_of_vertices,
            (index + 2) % number_of_vertices,
        )
        for index in range(number_of_triangles)
    ]


@pytest.mark.performance
def test_decode_point_set_1000_points_performance():
    """Ensure decoding 1,000 points stays below the regression threshold."""
    points = generate_points(1000)
    binary_data = encode_point_set(points)

    median_time = measure_median(
        lambda: decode_point_set(binary_data),
    )

    assert median_time < MAX_DECODE_TIME, (
        f"Decoding 1000 points took {median_time:.4f}s; "
        f"maximum allowed is {MAX_DECODE_TIME}s"
    )


@pytest.mark.performance
def test_encode_triangle_set_performance():
    """Ensure encoding 1,000 vertices and 2,000 triangles stays fast."""
    vertices = generate_points(1000)
    triangles = generate_triangles(
        number_of_vertices=1000,
        number_of_triangles=2000,
    )

    median_time = measure_median(
        lambda: encode_triangle_set(vertices, triangles),
    )

    assert median_time < MAX_ENCODE_TIME, (
        f"Encoding 1000 vertices and 2000 triangles took "
        f"{median_time:.4f}s; maximum allowed is {MAX_ENCODE_TIME}s"
    )