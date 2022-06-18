from flask import Flask, Blueprint, request
from flask.templating import render_template
from utils import *
import json

bp = Blueprint('main', __name__, url_prefix='/')
configs = json.load(open("setting.conf", "r"))
ResourceManager = configs["RM-IP:Port"] if "RM-IP:Port" in configs else "localhost:8088"
ApplicationMaster = configs["AM-IP:Port"] if "AM-IP:Port" in configs else "localhost:8088"
interval = configs["update-interval"] if "update-interval" in configs else "5"
worker_file = configs["workers"] if "workers" in configs else "./workers"
with open(worker_file, "r") as f:
    workers = [node.strip() for node in f.readlines()]

@bp.route('/')
def index():
    app_list = get_apps(ResourceManager, "RUNNING")
    
    data = {"workers": workers, "apps": app_list, "AM": ApplicationMaster, "interval": interval}
    return render_template('index.html', data=data)


app = Flask(__name__)
app.register_blueprint(bp)
app.run("127.0.0.1", port="4000", debug=True)
