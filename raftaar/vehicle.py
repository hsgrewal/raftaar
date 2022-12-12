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

bp = Blueprint('vehicle', __name__, url_prefix='/vehicle')


@bp.route('/')
@login_required
def index():
    db = get_db()
    query = f"""SELECT v.id, name, vin, license_plate, year, make, model,
        first_name || ' ' || last_name as owner FROM vehicle v
        JOIN user u ON v.owner_id = u.id WHERE v.owner_id = {g.user['id']}"""
    vehicles = db.execute(query).fetchall()
    return render_template('vehicle/vehicle.html', vehicles=vehicles)


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        result = post_action(Action.create)
        if result is not None:
            flash(result, Color.danger.name)
        else:
            return redirect(url_for('vehicle.index'))

    return render_template('vehicle/add.html')


def get_vehicle(id, check_owner=True):
    query = f"""SELECT v.id, owner_id, name, vin, license_plate, year, make,
        model FROM vehicle v JOIN user u ON v.owner_id = u.id
        WHERE v.id = {id}"""
    vehicle = get_db().execute(query).fetchone()

    if vehicle is None:
        abort(404, f'Vehicle id {id} does not exist')

    if check_owner and vehicle['owner_id'] != g.user['id']:
        abort(403)

    return vehicle


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    vehicle = get_vehicle(id)

    if request.method == 'POST':
        result = post_action(Action.update, id)
        if result is not None:
            flash(result, Color.danger.name)
        else:
            return redirect(url_for('vehicle.index'))

    return render_template('vehicle/edit.html', vehicle=vehicle)


@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    get_vehicle(id)
    query = f"DELETE FROM vehicle WHERE id = {id}"
    run_query(query)
    return redirect(url_for('vehicle.index'))


def post_action(action, id=1):
    name = request.form['name']
    vin = request.form['vin']
    license_plate = request.form['licensePlate']
    year = request.form['year']
    make = request.form['make']
    model = request.form['model']

    if not name:
        return 'Name is required'
    if not vin:
        return 'VIN is required'
    if not license_plate:
        return 'License Plate is required'
    if not year:
        return 'Year is required'
    if not make:
        return 'Make is required'
    if not model:
        return 'Model is required'

    if action is Action.create:
        query = f"""INSERT INTO vehicle
            (owner_id, name, vin, license_plate, year, make, model)
            VALUES ({g.user['id']}, '{name}', '{vin}', '{license_plate}',
            '{year}', '{make}', '{model}')"""
    else:
        query = f"""UPDATE vehicle SET name = '{name}', vin = '{vin}',
            license_plate = '{license_plate}', year = '{year}',
            make = '{make}', model = '{model}' WHERE id = {id}"""

    run_query(query)
    return None
