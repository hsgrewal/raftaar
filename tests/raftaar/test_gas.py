import pytest

def test_index(client, auth):
    auth.login()
    response = client.get('/gas/')
    assert response.status_code == 200
    assert b'href="/gas/add"' in response.data
    assert b'href="/gas/edit/1"' in response.data
