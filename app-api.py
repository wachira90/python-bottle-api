#!python
import os
import sys

from bottle import request, response
from bottle import post, get, put, delete
from bottle import Bottle, run, route, debug

import random
import re
import json

namepattern = re.compile(r'^[a-zA-Z\d]{1,64}$')

_names = set()

app = Bottle()


@app.route('/')
def hello():
    return "<h1>Hello World!<br>/rd<br>/arr</h1>"

@app.route('/rd')
def rd():
    from json import dumps
    min = 0
    max = 999
    user = 50
    digits = [str(random.randint(min, max)) for i in range(user)]
    digits = [(len(str(max))-len(digit))*'0'+digit for digit in digits] 
    # print(digits)
    return dumps(digits)

@app.route('/arr')
def returnarray():
    from bottle import response
    from json import dumps
    data = [{ "id": 1, "name": "Test Item 1" }, { "id": 2, "name": "Test Item 2" }]
    response.content_type = 'application/json'
    return dumps(data)


@post('/names')
def creation_handler():
    '''Handles name creation'''
    try:
        # parse input data
        try:
            data = request.json()
        except:
            raise ValueError

        if data is None:
            raise ValueError

        # extract and validate name
        try:
            if namepattern.match(data['name']) is None:
                raise ValueError
            name = data['name']
        except (TypeError, KeyError):
            raise ValueError

        # check for existence
        if name in _names:
            raise KeyError

    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return

    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return

    # add name
    _names.add(name)

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'name': name})


run(app, host='localhost', port=7000, reloader=True, debug=True)
