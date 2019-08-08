#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

import os
import sys
import logging
logger = logging.getLogger('webui')


from flask import Flask, render_template
from flask import request
from flask_script import Manager

app = Flask(__name__)

# manager = Manager(app)


@app.route('/')
def index():
    osName = os.name
    userAgent = request.headers.get('User-Agent')
    return render_template('index.html', osName=osName)

@app.route('/user/<name>')
def user(name):
    return '<h1>hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
    # manager.run()
