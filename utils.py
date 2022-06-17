import requests

def convert_response(response):
    if 'application/json' in response.headers['Content-Type']:
        return response.json()
    else:
        return response.text

def get_apps(RM, status):
    response = requests.get(f"http://{RM}/cluster/apps/{status}")
    result = convert_response(response)
    
    flg = False
    apps = []
    for line in result.split('\n'):
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
