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
    workers = sorted(node.strip() for node in f.readlines())

@bp.route('/')
def index():
    app_list = get_apps(ResourceManager, "RUNNING")
    
    tasks = [[], []]
    if len(app_list) > 0:
        tasks = get_tasks(ApplicationMaster, app_list[0][0])
    
    map_tasks = {node:[] for node in workers}
    for task in tasks[0]:
        map_tasks[task[4]].append(int(task[1]))
    mappers = [sorted(map_tasks[node], reverse=True) for node in workers]

    reduce_tasks = {node:[] for node in workers}
    for task in tasks[1]:
        reduce_tasks[task[4]].append(int(task[1]))
    reducers = [sorted(reduce_tasks[node], reverse=True) for node in workers]

    data = {"workers": workers, "apps": app_list, "mappers": mappers, "reducers": reducers, "interval": interval}
    return render_template('index.html', data=data)

@bp.route('/<target_app_id>')
def application(target_app_id):
    app_list = get_apps(ResourceManager, "RUNNING")
    
    tasks = [[], []]
    for app_id, _ in app_list:
        if app_id == target_app_id:
            tasks = get_tasks(ApplicationMaster, app_id)
            break
            
    map_tasks = {node:[] for node in workers}
    for task in tasks[0]:
        map_tasks[task[4]].append(int(task[1]))
    mappers = [sorted(map_tasks[node], reverse=True) for node in workers]

    reduce_tasks = {node:[] for node in workers}
    for task in tasks[1]:
        reduce_tasks[task[4]].append(int(task[1]))
    reducers = [sorted(reduce_tasks[node], reverse=True) for node in workers]

    data = {"workers": workers, "apps": app_list, "mappers": mappers, "reducers": reducers, "interval": interval}
    return render_template('index.html', data=data)


app = Flask(__name__)
app.register_blueprint(bp)
app.run("127.0.0.1", port="4000", debug=True)
