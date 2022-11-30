from flask import Blueprint, render_template

bp_main = Blueprint('bp_main', __name__)


@bp_main.route("/")
def upload_file():
    return render_template('formulario.html')