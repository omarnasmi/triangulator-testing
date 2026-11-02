"""End-to-end tests for the Triangulator service."""

from decoder import decode_triangle_set


def test_complete_triangulation_flow(
    point_set_manager,
    triangulator_client,
):
    """Verify the complete PointSetManager-to-Triangulator workflow."""
    points = [
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 1.0),
    ]

    point_set_id = point_set_manager.create_point_set(points)

    response = triangulator_client.get(
        f"/triangulation/{point_set_id}",
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"

    vertices, triangles = decode_triangle_set(response.content)

    assert vertices == points
    assert len(triangles) == 2

    for triangle in triangles:
        assert len(triangle) == 3
        assert len(set(triangle)) == 3
        assert all(0 <= index < len(vertices) for index in triangle)
