"""This module tests the `/ticket` endpoint."""
import json
import pytest

def _get_expected_response():
    return """
    {
        "ticket": ""
    }
    """

@pytest.mark.django_db
def test_book_flight(client)
    response = client.get(f"/ticket/book", follow=True)
    content = json.loads(response.content)
    expected_response = json.loads(_get_expected_response())
    assert content == expected_response
    assert response.status_code == 200