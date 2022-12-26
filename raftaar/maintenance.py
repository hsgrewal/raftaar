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

bp = Blueprint('maintenance', __name__, url_prefix='/maintenance')


@bp.route('/')
@login_required
def index():
    db = get_db()
    query = f"""SELECT m.id, vehicle_id, strftime('%m/%d/%Y', date) as date,
        cost, mileage, memo, type, name FROM maintenance m
        JOIN vehicle v ON m.vehicle_id = v.id
        WHERE v.owner_id = {g.user['id']}"""
    maintenance = db.execute(query).fetchall()
    return render_template('maintenance/index.html', maintenance=maintenance)


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        result = post_action(Action.create)
        if result is not None:
            flash(result, Color.danger.name)
        else:
            return redirect(url_for('maintenance.index'))

    return render_template('maintenance/add.html')


def get_maintenance(id, check_vehicle=True):
    query = f"""SELECT m.id, vehicle_id, date, cost, mileage, memo, type,
        strftime('%m/%d/%Y', date) as fdate FROM maintenance m
        JOIN vehicle v ON m.vehicle_id = v.id WHERE m.id = {id}"""
    maintenance = get_db().execute(query).fetchone()

    if maintenance is None:
        abort(404, f'Maintenance id {id} does not exist')

    if check_vehicle and maintenance['vehicle_id'] != 1:
        abort(403)

    return maintenance


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    maintenance = get_maintenance(id)

    if request.method == 'POST':
        result = post_action(Action.update, id)
        if result is not None:
            flash(result, Color.danger.name)
        else:
            return redirect(url_for('maintenance.index'))

    return render_template('maintenance/edit.html', maintenance=maintenance)


@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    get_maintenance(id)
    query = f"DELETE FROM maintenance WHERE id = {id}"
    run_query(query)
    return redirect(url_for('maintenance.index'))


def post_action(action, id=1):
    date = request.form['date']
    cost = request.form['cost']
    mileage = request.form['mileage']
    memo = request.form['memo']
    type = request.form['type']

    if not date:
        return 'Date is required'
    if not cost:
        return 'Cost is required'
    if not mileage:
        return 'Mileage is required'
    if not memo:
        return 'Memo is required'
    if not type:
        return 'Type is required'

    if action is Action.create:
        # TODO update query with vehicle_id
        query = f"""INSERT INTO maintenance (vehicle_id, date, cost, mileage, memo, type)
            VALUES (1, '{date}', {cost}, {mileage}, '{memo}', '{type}')"""
    else:
        query = f"""UPDATE maintenance SET date = '{date}', cost = {cost},
            mileage = {mileage}, memo = '{memo}', type = '{type}' WHERE id = {id}"""

    run_query(query)
    return None
