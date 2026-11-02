import struct

import pytest

from decoder import decode_point_set, decode_triangle_set
from encoder import encode_point_set, encode_triangle_set


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def point_set_binary(points):
    """Build the expected PointSet binary representation."""
    data = struct.pack("<I", len(points))

    for x, y in points:
        data += struct.pack("<ff", x, y)

    return data


def triangle_set_binary(vertices, triangles):
    """Build the expected Triangles binary representation."""
    data = point_set_binary(vertices)
    data += struct.pack("<I", len(triangles))

    for index_a, index_b, index_c in triangles:
        data += struct.pack("<III", index_a, index_b, index_c)

    return data


# ===========================================================================
# PointSet - encoding
# ===========================================================================


def test_encode_empty_point_set():
"""Test test encode empty point set."""
    points = []

    encoded = encode_point_set(points)

    assert encoded == struct.pack("<I", 0)


def test_encode_one_point():
"""Test test encode one point."""
    points = [(1.0, 2.0)]

    encoded = encode_point_set(points)

    expected = point_set_binary(points)

    assert encoded == expected


def test_encode_multiple_points():
"""Test test encode multiple points."""
    points = [
        (0.0, 0.0),
        (10.0, 20.0),
        (-5.5, 3.25),
    ]

    encoded = encode_point_set(points)

    expected = point_set_binary(points)

    assert encoded == expected


def test_encode_positive_negative_and_decimal_coordinates():
"""Test test encode positive negative and decimal coordinates."""
    points = [
        (1.5, 2.75),
        (-10.25, 5.5),
        (100.125, -200.625),
    ]

    encoded = encode_point_set(points)

    expected = point_set_binary(points)

    assert encoded == expected


# ===========================================================================
# PointSet - decoding
# ===========================================================================


def test_decode_empty_point_set():
"""Test test decode empty point set."""
    binary_data = struct.pack("<I", 0)

    decoded = decode_point_set(binary_data)

    assert decoded == []


def test_decode_one_point():
"""Test test decode one point."""
    points = [(1.0, 2.0)]

    binary_data = point_set_binary(points)

    decoded = decode_point_set(binary_data)

    assert decoded == points


def test_decode_multiple_points():
"""Test test decode multiple points."""
    points = [
        (0.0, 0.0),
        (10.0, 20.0),
        (-5.5, 3.25),
    ]

    binary_data = point_set_binary(points)

    decoded = decode_point_set(binary_data)

    assert decoded == points


def test_decode_positive_negative_and_decimal_coordinates():
"""Test test decode positive negative and decimal coordinates."""
    points = [
        (1.5, 2.75),
        (-10.25, 5.5),
        (100.125, -200.625),
    ]

    binary_data = point_set_binary(points)

    decoded = decode_point_set(binary_data)

    assert decoded == points


# ===========================================================================
# PointSet - round trip
# ===========================================================================


def test_point_set_round_trip():
"""Test test point set round trip."""
    points = [
        (0.0, 0.0),
        (10.5, -20.25),
        (-3.75, 4.125),
        (100.0, 200.0),
    ]

    encoded = encode_point_set(points)
    decoded = decode_point_set(encoded)
    
    assert decoded == points


# ===========================================================================
# PointSet - invalid binary data
# ===========================================================================


def test_decode_point_set_rejects_binary_data_shorter_than_count():
"""Test test decode point set rejects binary data shorter than count."""
    binary_data = b"\x00\x00"

    with pytest.raises(ValueError):
        decode_point_set(binary_data)


def test_decode_point_set_rejects_incomplete_point():
    # Count says that one point exists, but no complete point follows.
"""Test test decode point set rejects incomplete point."""
    binary_data = struct.pack("<I", 1)

    with pytest.raises(ValueError):
        decode_point_set(binary_data)


def test_decode_point_set_rejects_incomplete_point_data():
    # Count = 1, but only 4 of the required 8 point bytes are present.
"""Test test decode point set rejects incomplete point data."""
    binary_data = struct.pack("<I", 1) + struct.pack("<f", 1.0)

    with pytest.raises(ValueError):
        decode_point_set(binary_data)


def test_decode_point_set_rejects_inconsistent_point_count():
    # Count says 2 points, but only one is present.
"""Test test decode point set rejects inconsistent point count."""
    points = [(1.0, 2.0)]

    binary_data = struct.pack("<I", 2)

    for x, y in points:
        binary_data += struct.pack("<ff", x, y)

    with pytest.raises(ValueError):
        decode_point_set(binary_data)


def test_decode_point_set_rejects_extra_data():
"""Test test decode point set rejects extra data."""
    points = [(1.0, 2.0)]

    binary_data = point_set_binary(points)
    binary_data += b"\x00"

    with pytest.raises(ValueError):
        decode_point_set(binary_data)


# ===========================================================================
# Triangles - encoding
# ===========================================================================


def test_encode_triangle_set_with_no_triangles():
"""Test test encode triangle set with no triangles."""
    vertices = [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 10.0),
    ]
    triangles = []

    encoded = encode_triangle_set(vertices, triangles)

    expected = triangle_set_binary(vertices, triangles)

    assert encoded == expected


def test_encode_triangle_set_with_one_triangle():
"""Test test encode triangle set with one triangle."""
    vertices = [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 10.0),
    ]
    triangles = [
        (0, 1, 2),
    ]

    encoded = encode_triangle_set(vertices, triangles)

    expected = triangle_set_binary(vertices, triangles)

    assert encoded == expected


def test_encode_triangle_set_with_multiple_triangles():
"""Test test encode triangle set with multiple triangles."""
    vertices = [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 10.0),
        (0.0, 10.0),
    ]
    triangles = [
        (0, 1, 2),
        (0, 2, 3),
    ]

    encoded = encode_triangle_set(vertices, triangles)

    expected = triangle_set_binary(vertices, triangles)

    assert encoded == expected


# ===========================================================================
# Triangles - decoding
# ===========================================================================


def test_decode_triangle_set_with_no_triangles():
"""Test test decode triangle set with no triangles."""
    vertices = [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 10.0),
    ]
    triangles = []

    binary_data = triangle_set_binary(vertices, triangles)

    decoded_vertices, decoded_triangles = decode_triangle_set(binary_data)

    assert decoded_vertices == vertices
    assert decoded_triangles == triangles


def test_decode_triangle_set_with_one_triangle():
"""Test test decode triangle set with one triangle."""
    vertices = [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 10.0),
    ]
    triangles = [
        (0, 1, 2),
    ]

    binary_data = triangle_set_binary(vertices, triangles)

    decoded_vertices, decoded_triangles = decode_triangle_set(binary_data)

    assert decoded_vertices == vertices
    assert decoded_triangles == triangles


def test_decode_triangle_set_with_multiple_triangles():
"""Test test decode triangle set with multiple triangles."""
    vertices = [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 10.0),
        (0.0, 10.0),
    ]
    triangles = [
        (0, 1, 2),
        (0, 2, 3),
    ]

    binary_data = triangle_set_binary(vertices, triangles)

    decoded_vertices, decoded_triangles = decode_triangle_set(binary_data)

    assert decoded_vertices == vertices
    assert decoded_triangles == triangles


# ===========================================================================
# Triangles - vertices preservation
# ===========================================================================


def test_triangle_set_preserves_vertices():
"""Test test triangle set preserves vertices."""
    vertices = [
        (-10.5, 20.25),
        (30.75, -40.125),
        (50.0, 60.5),
    ]
    triangles = [
        (0, 1, 2),
    ]

    encoded = encode_triangle_set(vertices, triangles)
    decoded_vertices, _ = decode_triangle_set(encoded)

    assert decoded_vertices == vertices


# ===========================================================================
# Triangles - triangle count
# ===========================================================================


def test_triangle_set_preserves_triangle_count():
"""Test test triangle set preserves triangle count."""
    vertices = [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 10.0),
        (0.0, 10.0),
    ]
    triangles = [
        (0, 1, 2),
        (0, 2, 3),
    ]

    encoded = encode_triangle_set(vertices, triangles)
    _, decoded_triangles = decode_triangle_set(encoded)

    assert len(decoded_triangles) == len(triangles)


# ===========================================================================
# Triangles - valid indices
# ===========================================================================


def test_triangle_indices_reference_existing_vertices():
"""Test test triangle indices reference existing vertices."""
    vertices = [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 10.0),
        (0.0, 10.0),
    ]
    triangles = [
        (0, 1, 2),
        (0, 2, 3),
    ]

    encoded = encode_triangle_set(vertices, triangles)
    decoded_vertices, decoded_triangles = decode_triangle_set(encoded)

    for triangle in decoded_triangles:
        for index in triangle:
            assert 0 <= index < len(decoded_vertices)


# ===========================================================================
# Triangles - round trip
# ===========================================================================


def test_triangle_set_round_trip():
"""Test test triangle set round trip."""
    vertices = [
        (0.0, 0.0),
        (10.5, -20.25),
        (-3.75, 4.125),
        (100.0, 200.0),
    ]
    triangles = [
        (0, 1, 2),
        (0, 2, 3),
    ]

    encoded = encode_triangle_set(vertices, triangles)
    decoded_vertices, decoded_triangles = decode_triangle_set(encoded)

    assert decoded_vertices == vertices
    assert decoded_triangles == triangles


# ===========================================================================
# Triangles - invalid binary data
# ===========================================================================


def test_decode_triangle_set_rejects_binary_data_shorter_than_vertex_count():
"""Test test decode triangle set rejects binary data shorter than vertex count."""
    binary_data = b"\x00\x00"

    with pytest.raises(ValueError):
        decode_triangle_set(binary_data)


def test_decode_triangle_set_rejects_incomplete_vertex():
    # One vertex is declared, but no vertex data is provided.
"""Test test decode triangle set rejects incomplete vertex."""
    binary_data = struct.pack("<I", 1)

    with pytest.raises(ValueError):
        decode_triangle_set(binary_data)


def test_decode_triangle_set_rejects_incomplete_triangle_count():
"""Test test decode triangle set rejects incomplete triangle count."""
    vertices = [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 10.0),
    ]

    binary_data = point_set_binary(vertices)

    with pytest.raises(ValueError):
        decode_triangle_set(binary_data)


def test_decode_triangle_set_rejects_incomplete_triangle():
"""Test test decode triangle set rejects incomplete triangle."""
    vertices = [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 10.0),
    ]

    binary_data = point_set_binary(vertices)
    binary_data += struct.pack("<I", 1)

    # A triangle requires 12 bytes, but only 8 are provided.
    binary_data += struct.pack("<II", 0, 1)

    with pytest.raises(ValueError):
        decode_triangle_set(binary_data)


def test_decode_triangle_set_rejects_inconsistent_triangle_count():
"""Test test decode triangle set rejects inconsistent triangle count."""
    vertices = [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 10.0),
    ]

    binary_data = point_set_binary(vertices)

    # Says there are two triangles...
    binary_data += struct.pack("<I", 2)

    # ...but only one is present.
    binary_data += struct.pack("<III", 0, 1, 2)

    with pytest.raises(ValueError):
        decode_triangle_set(binary_data)


def test_decode_triangle_set_rejects_extra_data():
"""Test test decode triangle set rejects extra data."""
    vertices = [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 10.0),
    ]
    triangles = [
        (0, 1, 2),
    ]

    binary_data = triangle_set_binary(vertices, triangles)
    binary_data += b"\x00"

    with pytest.raises(ValueError):
        decode_triangle_set(binary_data)


# ===========================================================================
# Triangles - invalid vertex indices
# ===========================================================================


def test_decode_triangle_set_rejects_vertex_index_out_of_range():
"""Test test decode triangle set rejects vertex index out of range."""
    vertices = [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 10.0),
    ]

    # Vertex indices 0, 1, 3 are invalid because only vertices
    # 0, 1 and 2 exist.
    triangles = [
        (0, 1, 3),
    ]

    binary_data = triangle_set_binary(vertices, triangles)

    with pytest.raises(ValueError):
        decode_triangle_set(binary_data)