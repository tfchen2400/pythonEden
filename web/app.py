#!/usr/bin/env python3
# coding=utf-8
import simplejson
from flask import Flask, jsonify, make_response, request
from flask_httpauth import HTTPBasicAuth
import json

from dcap_db.Dcap_main import Dcap_main
import uuid

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World! maps is on \"/todo/api/v1.0/maps\""


auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'ok':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


maps = [
    {
        'id': 1,
        'title': u'do all',
        'description': u'执行一切',
        'url': "execAll"
    }
]


@app.route('/todo/api/v1.0/maps', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'maps': maps})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/execAll', methods=['GET'])
@auth.login_required
def exec_all():
    info = request.args['info']
    ret_dict = simplejson.loads(info)
    ret_dict["uuid"] = str(uuid.uuid1())
    jsoninfo = simplejson.dumps(ret_dict)

    dcap_main = Dcap_main()
    resultInfo = dcap_main.exec_all(jsoninfo)

    return jsonify({'resultInfo': resultInfo})


if __name__ == '__main__':
    # print(uuid.uuid1())
    app.run(host='0.0.0.0', debug=True)
    #app.run(debug=True)
