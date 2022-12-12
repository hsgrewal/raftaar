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

bp = Blueprint('gas', __name__, url_prefix='/gas')


@bp.route('/')
@login_required
def index():
    db = get_db()
    query = f"""SELECT g.id, vehicle_id, strftime('%m/%d/%Y', date) as date, gallons, cost,
        mileage, name FROM gas g JOIN vehicle v ON g.vehicle_id = v.id
        WHERE v.owner_id = {g.user['id']}"""
    gas = db.execute(query).fetchall()
    return render_template('gas/index.html', gas=gas)


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        result = post_action(Action.create)
        if result is not None:
            flash(result, Color.danger.name)
        else:
            return redirect(url_for('gas.index'))


    return render_template('gas/add.html')


def get_gas(id, check_vehicle=True):
    query = f"""SELECT g.id, vehicle_id, date, gallons, cost, mileage,
        strftime('%m/%d/%Y', date) as fdate FROM gas g
        JOIN vehicle v ON g.vehicle_id = v.id WHERE g.id = {id}"""
    gas = get_db().execute(query).fetchone()

    if gas is None:
        abort(404, f'Gas id {id} does not exist')

    if check_vehicle and gas['vehicle_id'] != 1:
        abort(403)

    return gas


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    gas = get_gas(id)

    if request.method == 'POST':
        result = post_action(Action.update, id)
        if result is not None:
            flash(result, Color.danger.name)
        else:
            return redirect(url_for('gas.index'))

    return render_template('gas/edit.html', gas=gas)


@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    get_gas(id)
    query = f"DELETE FROM gas WHERE id = {id}"
    run_query(query)
    return redirect(url_for('gas.index'))


def post_action(action, id=1):
    date = request.form['date']
    gallons = request.form['gallons']
    cost = request.form['cost']
    mileage = request.form['mileage']

    if not date:
        return 'Date is required'
    if not gallons:
        return 'Gallons is required'
    if not cost:
        return 'Cost is required'
    if not mileage:
        return 'Mileage is required'

    if action is Action.create:
        # TODO update query with vehicle_id
        query = f"""INSERT INTO gas (vehicle_id, date, gallons, cost, mileage)
            VALUES (1, '{date}', {gallons}, {cost}, {mileage})"""
    else:
        query = f"""UPDATE gas SET date = '{date}', gallons = {gallons},
            cost = {cost}, mileage = {mileage} WHERE id = {id}"""

    run_query(query)
    return None
