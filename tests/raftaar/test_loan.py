import pytest
from raftaar.db import get_db, run_query


def test_index(client, auth):
    auth.login()
    response = client.get('/loan/')
    assert response.status_code == 200
    assert b'href="/loan/add"' in response.data
    assert b'href="/loan/edit/1"' in response.data


def test_index_no_loan(app, client, auth):
    # change loan to another vehicle
    with app.app_context():
        query = 'UPDATE loan SET vehicle_id = 2 WHERE id = 1'
        run_query(query)

    auth.login()
    response = client.get('/loan/')
    assert b'No loan payments found. Please add one.' in response.data
    assert b'href="/loan/add"' in response.data


def test_index_no_login(client):
    response = client.get('/loan/')
    assert b'Redirecting' in response.data
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize('path', (
    '/loan/add',
    '/loan/edit/1',
    '/loan/delete/1',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_vehicle_required(app, client, auth):
    # change loan to another vehicle
    with app.app_context():
        query = 'UPDATE loan SET vehicle_id = 2 WHERE id = 1'
        run_query(query)

    auth.login()
    # current vehicle cannot modify other vehicle's loan transactions
    assert client.post('/loan/edit/1').status_code == 403
    assert client.post('/loan/delete/1').status_code == 403
    # current vehicle should not see edit nor delete links for other loan
    assert b'href="/loan/edit/1"' not in client.get('/loan/').data
    assert b'href="/loan/delete/1"' not in client.get('/loan/').data


@pytest.mark.parametrize('path', (
    '/loan/edit/2',
    '/loan/delete/2',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_add(client, auth, app):
    auth.login()
    assert client.get('/loan/add').status_code == 200
    client.post('/loan/add', data={
        'date': '2022-12-19',
        'amount': 325.45,
        'memo': 'Test Memo'
    })

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM loan').fetchone()[0]
        assert count == 2


def test_edit(client, auth, app):
    auth.login()
    assert client.get('/loan/edit/1').status_code == 200
    client.post('/loan/edit/1', data={
        'date': '2022-12-19',
        'amount': 525.63,
        'memo': 'Test Memo'
    })

    with app.app_context():
        db = get_db()
        loan = db.execute('SELECT * FROM loan WHERE id = 1').fetchone()
        assert loan['date'] == '2022-12-19'
        assert loan['amount'] == 525.63
        assert loan['memo'] == 'Test Memo'


@pytest.mark.parametrize(('path', 'date', 'amount', 'memo', 'message'), (
    ('/loan/add', '', '', '', b'Date is required'),
    ('/loan/add', '2022-12-19', '', '', b'Amount is required'),
    ('/loan/add', '2022-12-19', '313.68', '', b'Memo is required'),
    ('/loan/edit/1', '', '', '', b'Date is required'),
    ('/loan/edit/1', '2022-12-19', '', '', b'Amount is required'),
    ('/loan/edit/1', '2022-12-19', '313.68', '', b'Memo is required')
))
def test_create_update_validate(client, auth, path, date, amount, memo, message):
    auth.login()
    response = client.post(path, data={
        'date': date,
        'amount': amount,
        'memo': memo
    })
    assert message in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/loan/delete/1')
    assert response.headers["Location"] == "/loan/"

    with app.app_context():
        db = get_db()
        loan = db.execute('SELECT * FROM loan WHERE id = 1').fetchone()
        assert loan is None
