import pytest
from raftaar.db import get_db, run_query


def test_index(client, auth):
    auth.login()
    response = client.get('/maintenance/')
    assert response.status_code == 200
    assert b'href="/maintenance/add"' in response.data
    assert b'href="/maintenance/edit/1"' in response.data


def test_index_no_gas(app, client, auth):
    # change maintenance to another vehicle
    with app.app_context():
        query = 'UPDATE maintenance SET vehicle_id = 2 WHERE id = 1'
        run_query(query)

    auth.login()
    response = client.get('/maintenance/')
    assert b'No maintenance found. Please add one.' in response.data
    assert b'href="/maintenance/add"' in response.data


def test_index_no_login(client):
    response = client.get('/maintenance/')
    assert b'Redirecting' in response.data
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize('path', (
    '/maintenance/add',
    '/maintenance/edit/1',
    '/maintenance/delete/1',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_vehicle_required(app, client, auth):
    # change maintenance to another vehicle
    with app.app_context():
        query = 'UPDATE maintenance SET vehicle_id = 2 WHERE id = 1'
        run_query(query)

    auth.login()
    # current vehicle cannot modify other vehicle's maintenance transactions
    assert client.post('/maintenance/edit/1').status_code == 403
    assert client.post('/maintenance/delete/1').status_code == 403
    # current vehicle should not see edit nor delete links for other maintenance
    assert b'href="/maintenance/edit/1"' not in client.get('/maintenance/').data
    assert b'href="/maintenance/delete/1"' not in client.get('/maintenance/').data


@pytest.mark.parametrize('path', (
    '/maintenance/edit/2',
    '/maintenance/delete/2',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_add(client, auth, app):
    auth.login()
    assert client.get('/maintenance/add').status_code == 200
    client.post('/maintenance/add', data={
        'date': '2022-12-19',
        'cost': 365.24,
        'mileage': 65000,
        'memo': 'Test Maintenance',
        'type': 'Test type'
    })

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM maintenance').fetchone()[0]
        assert count == 2


def test_edit(client, auth, app):
    auth.login()
    assert client.get('/maintenance/edit/1').status_code == 200
    client.post('/maintenance/edit/1', data={
        'date': '2022-12-19',
        'cost': 365.24,
        'mileage': 65000,
        'memo': 'Test Maintenance',
        'type': 'Test type'
    })

    with app.app_context():
        db = get_db()
        maintenance = db.execute('SELECT * FROM maintenance WHERE id = 1').fetchone()
        assert maintenance['date'] == '2022-12-19'
        assert maintenance['cost'] == 365.24
        assert maintenance['mileage'] == 65000
        assert maintenance['memo'] == 'Test Maintenance'
        assert maintenance['type'] == 'Test type'


@pytest.mark.parametrize(('path', 'date', 'cost', 'mileage', 'memo', 'type', 'message'), (
    ('/maintenance/add', '', '', '', '', '', b'Date is required'),
    ('/maintenance/add', '2022-12-19', '', '', '', '', b'Cost is required'),
    ('/maintenance/add', '2022-12-19', '365.24', '', '', '', b'Mileage is required'),
    ('/maintenance/add', '2022-12-19', '365.24', '65000', '', '', b'Memo is required'),
    ('/maintenance/add', '2022-12-19', '365.24', '65000', 'Test', '', b'Type is required'),
    ('/maintenance/edit/1', '', '', '', '', '', b'Date is required'),
    ('/maintenance/edit/1', '2022-12-19', '', '', '', '', b'Cost is required'),
    ('/maintenance/edit/1', '2022-12-19', '365.24', '', '', '', b'Mileage is required'),
    ('/maintenance/edit/1', '2022-12-19', '365.24', '65000', '', '', b'Memo is required'),
    ('/maintenance/edit/1', '2022-12-19', '365.24', '65000', 'Test', '', b'Type is required'),
))
def test_create_update_validate(
        client, auth, path, date, cost, mileage, memo, type, message
    ):
    auth.login()
    response = client.post(path, data={
        'date': date,
        'cost': cost,
        'mileage': mileage,
        'memo': memo,
        'type': type
    })
    assert message in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/maintenance/delete/1')
    assert response.headers["Location"] == "/maintenance/"

    with app.app_context():
        db = get_db()
        maintenance = db.execute('SELECT * FROM maintenance WHERE id = 1').fetchone()
        assert maintenance is None
