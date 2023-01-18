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

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')
