#!/usr/bin/env python3
# coding: utf-8
__version__     = '0.0.1'
__author__      = 'Mateusz Jaromi, mateusz.jaromi@gmail.com'
__description__ = 'Public endpoint for BMC Discovery (ADDM) Generic Search Query'

import sys
sys.path.append('/usr/tideway/bin-custom/modules/python/certifi-2020.12.5')
sys.path.append('/usr/tideway/bin-custom/modules/python/chardet-4.0.0')
sys.path.append('/usr/tideway/bin-custom/modules/python/click-7.1.2/src')
sys.path.append('/usr/tideway/bin-custom/modules/python/Flask-1.1.2/src')
sys.path.append('/usr/tideway/bin-custom/modules/python/idna-3.1')
sys.path.append('/usr/tideway/bin-custom/modules/python/itsdangerous-1.1.0/src')
sys.path.append('/usr/tideway/bin-custom/modules/python/Jinja2-2.11.3/src')
sys.path.append('/usr/tideway/bin-custom/modules/python/MarkupSafe-1.1.1/src')
sys.path.append('/usr/tideway/bin-custom/modules/python/requests-2.25.1')
sys.path.append('/usr/tideway/bin-custom/modules/python/urllib3-1.26.4/src')
sys.path.append('/usr/tideway/bin-custom/modules/python/Werkzeug-1.0.1/src')
from flask import Flask, render_template, request, send_file
import io
import json
import os
import requests
import uuid

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

with open('config.json') as f:
    config = json.load(f)

FLASK_HOST = config['flask']['host']
FLASK_PORT = config['flask']['port']

API_ENDPOINT = 'https://' + config['appliance']['address'] + '/api/' + config['api']['version'] + '/' + config['api']['endpoint']

HEADERS = {
  'Authorization': 'Bearer {}'.format(config['api']['token']),
  'Content-Type': 'application/json'
}

app = Flask(__name__)


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def form_post():
    fileName = '{}.json'.format(uuid.uuid4().hex)
    filePath = '/tmp/{}'.format(fileName)
    
    payload = json.dumps({"query": request.form['text']})

    results = []
    call = json.loads(requests.post(API_ENDPOINT, headers=HEADERS, data=payload, verify=False).text)
    if not 'code' in call:
        for r in call[0]['results']:
            _dict = {}
            for h in range(len(call[0]['headings'])):
                _dict[call[0]['headings'][h]] = r[h]
            results.append(_dict)
        if 'next' in call[0]:
            while call[0]['next']:
                call=json.loads(requests.post(url=call[0]['next'], headers=HEADERS, data=payload, verify=False).text)
                for r in call[0]['results']:
                    _dict = {}
                    for h in range(len(call[0]['headings'])):
                        _dict[call[0]['headings'][h]] = r[h]
                    results.append(_dict)
                if not 'next' in call[0]:
                    break
    else:
        results = call

    with open(filePath, 'w') as f:
        f.write(json.dumps(results))

    return_data = io.BytesIO()
    with open(filePath, 'rb') as data:
        return_data.write(data.read())
    return_data.seek(0)
    os.remove(filePath)

    return send_file(return_data, as_attachment=True, attachment_filename=fileName, mimetype='application/json')


if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT)
