from flask import Flask, Blueprint, request
from flask.templating import render_template
import json

bp = Blueprint('main', __name__, url_prefix='/')
configs = json.load(open("cluster.conf", "r"))
ResourceManager = configs["RM-IP:Port"] if "RM-IP:Port" in configs else "localhost:8088"
ApplicationMaster = configs["AM-IP:Port"] if "AM-IP:Port" in configs else "localhost:8088"

@bp.route('/')
def index():
    return render_template('index.html')


app = Flask(__name__)
app.register_blueprint(bp)
app.run("127.0.0.1", port="4000", debug=True)
