import sqlite3

import pytest
from raftaar.db import get_db, run_query


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('raftaar.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called


@pytest.mark.parametrize(('query', 'result'), (
    ("INSERT INTO user (username, password, first_name, last_name) VALUES ('test', 'test', 'Carl', 'Sagan')", False),
    ("UPDATE user SET first_name = 'Issac', last_name = 'Newton' WHERE id = 1", True)
))
def test_run_query(app, query, result):
    with app.app_context():
        assert run_query(query) is result
