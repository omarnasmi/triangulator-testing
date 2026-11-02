import struct
from unittest.mock import Mock, patch

import pytest
import requests

from triangulator.point_set_manager import fetch_point_set


POINT_SET_ID = "123e4567-e89b-12d3-a456-426614174000"
POINT_SET_MANAGER_URL = "http://point-set-manager"


def encode_point_set(points):
    """Build valid PointSet binary data for tests."""
    data = bytearray(struct.pack("<I", len(points)))

    for x, y in points:
        data.extend(struct.pack("<ff", x, y))

    return bytes(data)


@patch("triangulator.point_set_manager.requests.get")
def test_fetch_point_set_returns_points_on_success(mock_get):
"""Test test fetch point set returns points on success."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]

    response = Mock()
    response.status_code = 200
    response.content = encode_point_set(points)
    mock_get.return_value = response

    result = fetch_point_set(POINT_SET_ID)

    assert result == points
    mock_get.assert_called_once()


@patch("triangulator.point_set_manager.requests.get")
def test_fetch_point_set_handles_not_found(mock_get):
"""Test test fetch point set handles not found."""
    response = Mock()
    response.status_code = 404
    mock_get.return_value = response

    with pytest.raises(PointSetNotFoundError):
        fetch_point_set(POINT_SET_ID)


@patch("triangulator.point_set_manager.requests.get")
def test_fetch_point_set_handles_bad_request(mock_get):
"""Test test fetch point set handles bad request."""
    response = Mock()
    response.status_code = 400
    mock_get.return_value = response

    with pytest.raises(Exception):
        fetch_point_set(POINT_SET_ID)


@patch("triangulator.point_set_manager.requests.get")
def test_fetch_point_set_handles_service_unavailable(mock_get):
"""Test test fetch point set handles service unavailable."""
    response = Mock()
    response.status_code = 503
    mock_get.return_value = response

    with pytest.raises(Exception):
        fetch_point_set(POINT_SET_ID)


@patch("triangulator.point_set_manager.requests.get")
def test_fetch_point_set_handles_connection_failure(mock_get):
"""Test test fetch point set handles connection failure."""
    mock_get.side_effect = requests.ConnectionError("Connection failed")

    with pytest.raises(Exception):
        fetch_point_set(POINT_SET_ID)


@patch("triangulator.point_set_manager.requests.get")
def test_fetch_point_set_handles_timeout(mock_get):
"""Test test fetch point set handles timeout."""
    mock_get.side_effect = requests.Timeout("Request timed out")

    with pytest.raises(Exception):
        fetch_point_set(POINT_SET_ID)


@patch("triangulator.point_set_manager.requests.get")
def test_fetch_point_set_rejects_incomplete_binary_data(mock_get):
"""Test test fetch point set rejects incomplete binary data."""
    response = Mock()
    response.status_code = 200

    # Declares one point but contains no point coordinates.
    response.content = struct.pack("<I", 1)
    mock_get.return_value = response

    with pytest.raises(Exception):
        fetch_point_set(POINT_SET_ID)


@patch("triangulator.point_set_manager.requests.get")
def test_fetch_point_set_rejects_inconsistent_point_count(mock_get):
    # Declares two points but contains coordinates for only one.
"""Test test fetch point set rejects inconsistent point count."""
    response = Mock()
    response.status_code = 200
    response.content = struct.pack("<Iff", 1, 2.0, 3.0)[:-1]
    mock_get.return_value = response

    with pytest.raises(Exception):
        fetch_point_set(POINT_SET_ID)


@patch("triangulator.point_set_manager.requests.get")
def test_fetch_point_set_requests_the_correct_point_set(mock_get):
"""Test test fetch point set requests the correct point set."""
    response = Mock()
    response.status_code = 200
    response.content = encode_point_set([(2.0, 3.0)])
    mock_get.return_value = response

    fetch_point_set(POINT_SET_ID)

    args, kwargs = mock_get.call_args
    assert args[0] == f"{POINT_SET_MANAGER_URL}/pointset/{POINT_SET_ID}"
