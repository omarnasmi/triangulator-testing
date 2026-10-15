import pytest

from triangulator.triangulation import triangulate


def triangle_area(points, triangle):
    """Calculate the absolute area of a triangle using vertex indices."""
    a, b, c = (points[index] for index in triangle)

    return abs(
        (b[0] - a[0]) * (c[1] - a[1])
        - (b[1] - a[1]) * (c[0] - a[0])
    ) / 2


def assert_valid_triangulation(points, triangles):
    """Check that every triangle uses valid, distinct, non-collinear vertices."""
    for triangle in triangles:
        assert len(triangle) == 3
        assert all(isinstance(index, int) for index in triangle)
        assert len(set(triangle)) == 3

        for index in triangle:
            assert 0 <= index < len(points)

        assert triangle_area(points, triangle) > 0


@pytest.mark.parametrize(
    "points",
    [
        [],
        [(0.0, 0.0)],
        [(0.0, 0.0), (1.0, 1.0)],
    ],
)
def test_fewer_than_three_points_produce_no_triangles(points):
    assert triangulate(points) == []


def test_three_non_collinear_points_form_one_triangle():
    points = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]

    triangles = triangulate(points)

    assert len(triangles) == 1
    assert_valid_triangulation(points, triangles)
    assert triangle_area(points, triangles[0]) == pytest.approx(0.5)


def test_four_points_forming_a_square_produce_two_triangles():
    points = [
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 1.0),
    ]

    triangles = triangulate(points)

    assert len(triangles) == 2
    assert_valid_triangulation(points, triangles)
    assert sum(triangle_area(points, t) for t in triangles) == pytest.approx(1.0)


def test_collinear_points_produce_no_triangles():
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]

    assert triangulate(points) == []


def test_duplicate_points_do_not_produce_degenerate_triangles():
    points = [
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (1.0, 1.0),
    ]

    triangles = triangulate(points)

    assert_valid_triangulation(points, triangles)


def test_negative_coordinates_are_supported():
    points = [(-1.0, -1.0), (1.0, -1.0), (0.0, 1.0)]

    triangles = triangulate(points)

    assert len(triangles) == 1
    assert_valid_triangulation(points, triangles)
    assert triangle_area(points, triangles[0]) == pytest.approx(2.0)


def test_decimal_coordinates_are_supported():
    points = [(0.1, 0.2), (1.3, 0.2), (0.7, 1.4)]

    triangles = triangulate(points)

    assert len(triangles) == 1
    assert_valid_triangulation(points, triangles)
    assert triangle_area(points, triangles[0]) == pytest.approx(0.72)


def test_points_with_zero_coordinates_are_supported():
    points = [(0.0, 0.0), (2.0, 0.0), (0.0, 2.0)]

    triangles = triangulate(points)

    assert len(triangles) == 1
    assert_valid_triangulation(points, triangles)
    assert triangle_area(points, triangles[0]) == pytest.approx(2.0)


def test_large_coordinates_are_handled():
    points = [
        (1_000_000.0, 1_000_000.0),
        (1_000_002.0, 1_000_000.0),
        (1_000_000.0, 1_000_002.0),
    ]

    triangles = triangulate(points)

    assert len(triangles) == 1
    assert_valid_triangulation(points, triangles)
    assert triangle_area(points, triangles[0]) == pytest.approx(2.0)


def test_triangulation_of_multiple_points():
    points = [
        (0.0, 0.0),
        (2.0, 0.0),
        (3.0, 1.0),
        (2.0, 3.0),
        (0.0, 2.0),
    ]

    triangles = triangulate(points)

    assert len(triangles) > 0
    assert_valid_triangulation(points, triangles)
    assert sum(triangle_area(points, t) for t in triangles) == pytest.approx(6.5)


def test_triangulation_of_points_inside_a_square():
    points = [
        (0.0, 0.0),
        (2.0, 0.0),
        (2.0, 2.0),
        (0.0, 2.0),
        (1.0, 1.0),
    ]

    triangles = triangulate(points)

    assert len(triangles) == 4
    assert_valid_triangulation(points, triangles)
    assert sum(triangle_area(points, t) for t in triangles) == pytest.approx(4.0)


def test_triangulation_of_points_on_a_grid():
    points = [
        (x, y)
        for y in range(3)
        for x in range(3)
    ]

    triangles = triangulate(points)

    assert len(triangles) == 8
    assert_valid_triangulation(points, triangles)
    assert sum(triangle_area(points, t) for t in triangles) == pytest.approx(4.0)


def test_triangulation_of_points_in_different_orders():
    points = [
        (0.0, 0.0),
        (2.0, 0.0),
        (2.0, 2.0),
        (0.0, 2.0),
        (1.0, 1.0),
    ]
    reordered_points = [points[i] for i in [4, 2, 0, 3, 1]]

    first_result = triangulate(points)
    second_result = triangulate(reordered_points)

    assert len(first_result) == len(second_result) == 4
    assert_valid_triangulation(points, first_result)
    assert_valid_triangulation(reordered_points, second_result)

    first_area = sum(triangle_area(points, t) for t in first_result)
    second_area = sum(
        triangle_area(reordered_points, t) for t in second_result
    )

    assert first_area == pytest.approx(4.0)
    assert second_area == pytest.approx(first_area)
