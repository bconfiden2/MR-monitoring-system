from flask import Flask, Blueprint, request
from flask.templating import render_template


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')


app = Flask(__name__)
app.register_blueprint(bp)
app.run("127.0.0.1", port="4000", debug=True)
