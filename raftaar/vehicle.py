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
from raftaar.db import get_db
from utils.enums import Color

bp = Blueprint('vehicle', __name__, url_prefix='/vehicle')


@bp.route('/')
@login_required
def index():
    db = get_db()
    query = f"SELECT name, vin, license_plate, year, make, model, first_name || ' ' || last_name as owner FROM vehicle v JOIN user u ON v.owner_id = u.id WHERE v.owner_id = {g.user['id']} ORDER BY year DESC"
    vehicles = db.execute(query).fetchall()
    return render_template('vehicle/vehicle.html', vehicles=vehicles)


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        name = request.form['name']
        vin = request.form['vin']
        license_plate = request.form['licensePlate']
        year = request.form['year']
        make = request.form['make']
        model = request.form['model']
        error = None

        if not name:
            error = 'Name is required'
        elif not vin:
            error = 'VIN is required'
        elif not license_plate:
            error = 'License Plate is required'
        elif not year:
            error = 'Year is required'
        elif not make:
            error = 'Make is required'
        elif not model:
            error = 'Model is required'

        if error is not None:
            flash(error, Color.warning.name)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO vehicle (owner_id, name, vin, license_plate, year, make, model)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (g.user['id'], name, vin, license_plate, year, make, model)
            )
            db.commit()
            return redirect(url_for('vehicle.index'))

    return render_template('vehicle/add.html')


# def get_post(id, check_author=True):
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, f"Post id {id} does not exist")

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)

#     return post


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required'

#         if error is not None:
#             flash(error, Color.warning.name)

#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ?'
#                 ' WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('index'))

#     return render_template('update.html', post=post)


# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('index'))
