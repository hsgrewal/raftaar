import pytest
from raftaar.db import get_db, run_query


def test_index(client, auth):
    auth.login()
    response = client.get('/gas/')
    assert response.status_code == 200
    assert b'href="/gas/add"' in response.data
    assert b'href="/gas/edit/1"' in response.data


def test_index_no_gas(app, client, auth):
    # change gas to another vehicle
    with app.app_context():
        query = 'UPDATE gas SET vehicle_id = 2 WHERE id = 1'
        run_query(query)

    auth.login()
    response = client.get('/gas/')
    assert b'No gas purchases found. Please add one.' in response.data
    assert b'href="/gas/add"' in response.data


def test_index_no_login(client):
    response = client.get('/gas/')
    assert b'Redirecting' in response.data
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize('path', (
    '/gas/add',
    '/gas/edit/1',
    '/gas/delete/1',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_vehicle_required(app, client, auth):
    # change gas to another vehicle
    with app.app_context():
        query = 'UPDATE gas SET vehicle_id = 2 WHERE id = 1'
        run_query(query)

    auth.login()
    # current vehicle cannot modify other vehicle's gas transactions
    assert client.post('/gas/edit/1').status_code == 403
    assert client.post('/gas/delete/1').status_code == 403
    # current vehicle should not see edit nor delete links for other gas
    assert b'href="/gas/edit/1"' not in client.get('/gas/').data
    assert b'href="/gas/delete/1"' not in client.get('/gas/').data


@pytest.mark.parametrize('path', (
    '/gas/edit/2',
    '/gas/delete/2',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_add(client, auth, app):
    auth.login()
    assert client.get('/gas/add').status_code == 200
    client.post('/gas/add', data={
        'date': '2022-12-19',
        'gallons': 1.25,
        'cost': 25.25,
        'mileage': 75000
    })

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM gas').fetchone()[0]
        assert count == 2


def test_edit(client, auth, app):
    auth.login()
    assert client.get('/gas/edit/1').status_code == 200
    client.post('/gas/edit/1', data={
        'date': '2022-12-19',
        'gallons': 1.254,
        'cost': 25.25,
        'mileage': 85000
    })

    with app.app_context():
        db = get_db()
        gas = db.execute('SELECT * FROM gas WHERE id = 1').fetchone()
        assert gas['date'] == '2022-12-19'
        assert gas['gallons'] == 1.254
        assert gas['cost'] == 25.25
        assert gas['mileage'] == 85000


@pytest.mark.parametrize(('path', 'date', 'gallons', 'cost', 'mileage', 'message'), (
    ('/gas/add', '', '', '', '', b'Date is required'),
    ('/gas/add', '2022-12-19', '', '', '', b'Gallons is required'),
    ('/gas/add', '2022-12-19', '1.254', '', '', b'Cost is required'),
    ('/gas/add', '2022-12-19', '1.254', '25.25', '', b'Mileage is required'),
    ('/gas/edit/1', '', '', '', '', b'Date is required'),
    ('/gas/edit/1', '2022-12-19', '', '', '', b'Gallons is required'),
    ('/gas/edit/1', '2022-12-19', '1.254', '', '', b'Cost is required'),
    ('/gas/edit/1', '2022-12-19', '1.254', '25.25', '', b'Mileage is required'),
))
def test_create_update_validate(
        client, auth, path, date, gallons, cost, mileage, message
    ):
    auth.login()
    response = client.post(path, data={
        'date': date,
        'gallons': gallons,
        'cost': cost,
        'mileage': mileage
    })
    assert message in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/gas/delete/1')
    assert response.headers["Location"] == "/gas/"

    with app.app_context():
        db = get_db()
        gas = db.execute('SELECT * FROM gas WHERE id = 1').fetchone()
        assert gas is None
