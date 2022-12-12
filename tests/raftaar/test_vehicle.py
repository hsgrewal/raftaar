import pytest
from raftaar.db import get_db, run_query


def test_index(client, auth):
    auth.login()
    response = client.get('/vehicle/')
    assert b'Raftaar' in response.data
    assert b'href="/vehicle/add"' in response.data
    assert b'href="/vehicle/edit/1"' in response.data


def test_index_no_vehicle(app, client, auth):
    # change vehicle owner to another user
    with app.app_context():
        query = 'UPDATE vehicle SET owner_id = 2 WHERE id = 1'
        run_query(query)

    auth.login()
    response = client.get('/vehicle/')
    assert b'No vehicle found. Please add one.' in response.data
    assert b'href="/vehicle/add"' in response.data


def test_index_no_login(client):
    response = client.get('/vehicle/')
    assert b'Redirecting' in response.data
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize('path', (
    '/vehicle/add',
    '/vehicle/edit/1',
    '/vehicle/delete/1',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    # change vehicle owner to another user
    with app.app_context():
        query = 'UPDATE vehicle SET owner_id = 2 WHERE id = 1'
        run_query(query)

    auth.login()
    # current user cannot modify other user's vehicles
    assert client.post('/vehicle/edit/1').status_code == 403
    assert client.post('/vehicle/delete/1').status_code == 403
    # current user should not see edit nor delete links for other vehicles
    assert b'href="/vehicle/edit/1"' not in client.get('/vehicle/').data
    assert b'href="/vehicle/delete/1"' not in client.get('/vehicle/').data


@pytest.mark.parametrize('path', (
    '/vehicle/edit/2',
    '/vehicle/delete/2',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


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


def test_edit(client, auth, app):
    auth.login()
    assert client.get('/vehicle/edit/1').status_code == 200
    client.post('/vehicle/edit/1', data={
        'name': 'Toofaan',
        'vin': 'test VIN',
        'licensePlate': 'test License Plate',
        'year': '1969',
        'make': 'Ford',
        'model': 'Mustang'
    })

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM vehicle WHERE id = 1').fetchone()
        assert post['name'] == 'Toofaan'


@pytest.mark.parametrize(
    ('path', 'name', 'vin', 'license_plate', 'year', 'make', 'model', 'message'), (
        ('/vehicle/add', '', '', '', '', '', '', b'Name is required'),
        ('/vehicle/add', 'a', '', '', '', '', '', b'VIN is required'),
        ('/vehicle/add', 'a', 'b', '', '', '', '', b'License Plate is required'),
        ('/vehicle/add', 'a', 'b', 'c', '', '', '', b'Year is required'),
        ('/vehicle/add', 'a', 'b', 'c', 'd', '', '', b'Make is required'),
        ('/vehicle/add', 'a', 'b', 'c', 'd', 'e', '', b'Model is required'),
        ('/vehicle/edit/1', '', '', '', '', '', '', b'Name is required'),
        ('/vehicle/edit/1', 'a', '', '', '', '', '', b'VIN is required'),
        ('/vehicle/edit/1', 'a', 'b', '', '', '', '', b'License Plate is required'),
        ('/vehicle/edit/1', 'a', 'b', 'c', '', '', '', b'Year is required'),
        ('/vehicle/edit/1', 'a', 'b', 'c', 'd', '', '', b'Make is required'),
        ('/vehicle/edit/1', 'a', 'b', 'c', 'd', 'e', '', b'Model is required'),
    )
)
def test_create_update_validate(
        client, auth, path, name, vin, license_plate, year, make, model, message
    ):
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


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/vehicle/delete/1')
    assert response.headers["Location"] == "/vehicle/"

    with app.app_context():
        db = get_db()
        vehicle = db.execute('SELECT * FROM vehicle WHERE id = 1').fetchone()
        assert vehicle is None
