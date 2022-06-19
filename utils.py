import requests

def convert_response(response):
    if 'application/json' in response.headers['Content-Type']:
        return response.json()
    else:
        return response.text

def preprocess(URL):
    response = requests.get(URL)
    result = convert_response(response)
    return result.split('\n')

def get_apps(RM, status):
    flg = False
    apps = []
    for line in preprocess(f"http://{RM}/cluster/apps/{status}"):
        if line.strip() == "var appsTableData=[":
            flg = True
            continue

        if not flg:
            continue

        if line[0] == ']':
            flg = False
            continue

        line = line[2:-2].split('","')
        app_id = '_'.join(line[0].split('_')[-2:])
        app_name = line[2]
        apps.append((app_id, app_name))

    return apps

def get_tasks(AM, app_id, task_flg):
    if task_flg not in ('m','r'):
        return []
    tasks = []
    flg = False
    for line in preprocess(f"http://{AM}/proxy/application_{app_id}/mapreduce/attempts/job_{app_id}/{task_flg}/RUNNING"):
        if line.strip() == "var attemptsTableData=[":
            flg = True
            continue

        if not flg:
            continue

        if line[0] == ']':
            flg = False
            continue

        line = line[1:-1].split(',')
        line[0] = '-'.join(line[0].split('>')[1].split('<')[0].split('_')[4:])
        line[1] = float(line[1][1:-1])
        line[2] = line[2]
        line[3] = "status"
        line[4] = line[4].split('>')[1].split('<')[0].split(':')[0]
    
        tasks.append(line[:5])

    return tasks
