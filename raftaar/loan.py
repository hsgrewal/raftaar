from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)
from werkzeug.exceptions import abort

from raftaar.auth import login_required
from raftaar.db import get_db, run_query
from utils.enums import Color, Action

bp = Blueprint('loan', __name__, url_prefix='/loan')


@bp.route('/')
@login_required
def index():
    db = get_db()
    query = f"""SELECT l.id, vehicle_id, strftime('%m/%d/%Y', date) as date,
        amount, memo, name FROM loan l JOIN vehicle v ON l.vehicle_id = v.id
        WHERE v.owner_id = {g.user['id']}"""
    loan = db.execute(query).fetchall()
    return render_template('loan/index.html', loan=loan)


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        result = post_action(Action.create)
        if result is not None:
            flash(result, Color.danger.name)
        else:
            return redirect(url_for('loan.index'))

    return render_template('loan/add.html')


def get_loan(id, check_vehicle=True):
    query = f"""SELECT l.id, vehicle_id, date, amount, memo,
        strftime('%m/%d/%Y', date) as fdate FROM loan l
        JOIN vehicle v ON l.vehicle_id = v.id WHERE l.id = {id}"""
    loan = get_db().execute(query).fetchone()

    if loan is None:
        abort(404, f'Loan id {id} does not exist')

    if check_vehicle and loan['vehicle_id'] != 1:
        abort(403)

    return loan


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    loan = get_loan(id)

    if request.method == 'POST':
        result = post_action(Action.update, id)
        if result is not None:
            flash(result, Color.danger.name)
        else:
            return redirect(url_for('loan.index'))

    return render_template('loan/edit.html', loan=loan)


@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    get_loan(id)
    query = f"DELETE FROM loan WHERE id = {id}"
    run_query(query)
    return redirect(url_for('loan.index'))


def post_action(action, id=1):
    date = request.form['date']
    amount = request.form['amount']
    memo = request.form['memo']

    if not date:
        return 'Date is required'
    if not amount:
        return 'Amount is required'
    if not memo:
        return 'Memo is required'

    if action is Action.create:
        # TODO update query with vehicle_id
        query = f"""INSERT INTO loan (vehicle_id, date, amount, memo)
            VALUES (1, '{date}', {amount}, '{memo}')"""
    else:
        query = f"""UPDATE loan SET date = '{date}', amount = {amount},
            memo = '{memo}' WHERE id = {id}"""

    run_query(query)
    return None
