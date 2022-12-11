import pytest
from raftaar.db import get_db


def test_index(client, auth):
    response = client.get('/vehicle/')
    assert b'Redirecting' in response.data

    auth.login()
    response = client.get('/vehicle/')
    assert b'No vehicle found. Please add one.' in response.data
    assert b'href="/vehicle/add"' in response.data


@pytest.mark.parametrize('path', (
    '/vehicle/add',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


# def test_author_required(app, client, auth):
#     # change post author to another user
#     with app.app_context():
#         db = get_db()
#         db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
#         db.commit()

#     auth.login()
#     # current user cannot modify other user's posts
#     assert client.post('/1/update').status_code == 403
#     assert client.post('/1/delete').status_code == 403
#     # current user should not see edit link
#     assert b'href="/1/update"' not in client.get('/').data


# @pytest.mark.parametrize('path', (
#     '/2/update',
#     '/2/delete',
# ))
# def test_exists_required(client, auth, path):
#     auth.login()
#     assert client.post(path).status_code == 404


def test_add(client, auth, app):
    auth.login()
    assert client.get('vehicle/add').status_code == 200
    client.post('vehicle/add', data={
        'name': 'Raftaar',
        'vin': 'test VIN',
        'licensePlate': 'test License Plate',
        'year': '1969',
        'make': 'Ford',
        'model': 'Mustang'
    })

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM vehicle').fetchone()[0]
        assert count == 2


# def test_update(client, auth, app):
#     auth.login()
#     assert client.get('/1/update').status_code == 200
#     client.post('/1/update', data={'title': 'updated', 'body': ''})

#     with app.app_context():
#         db = get_db()
#         post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
#         assert post['title'] == 'updated'


@pytest.mark.parametrize(('path', 'name', 'vin', 'license_plate', 'year', 'make', 'model', 'message'), (
    ('/vehicle/add', '', '', '', '', '', '', b'Name is required'),
    ('/vehicle/add', 'a', '', '', '', '', '', b'VIN is required'),
    ('/vehicle/add', 'a', 'b', '', '', '', '', b'License Plate is required'),
    ('/vehicle/add', 'a', 'b', 'c', '', '', '', b'Year is required'),
    ('/vehicle/add', 'a', 'b', 'c', 'd', '', '', b'Make is required'),
    ('/vehicle/add', 'a', 'b', 'c', 'd', 'e', '', b'Model is required'),
))
def test_create_update_validate(client, auth, path, name, vin, license_plate, year, make, model, message):
    auth.login()
    response = client.post(path, data={
        'name': name,
        'vin': vin,
        'licensePlate': license_plate,
        'year': year,
        'make': make,
        'model': model
    })
    assert message in response.data


# def test_delete(client, auth, app):
#     auth.login()
#     response = client.post('/1/delete')
#     assert response.headers["Location"] == "/"

#     with app.app_context():
#         db = get_db()
#         post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
#         assert post is None
