from flask import Flask, request, jsonify

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

import os
import json
import datetime

class LoginForm(FlaskForm):
    email = StringField(label='E-mail', validators=[
        validators.Email(),
        validators.DataRequired()
    ])

    password = PasswordField(label="Password", validators=[
        validators.Length(min=6),
        validators.DataRequired()
    ])

    pw_confirmation = PasswordField(label="Confirm password", validators=[
        validators.Length(min=6), 
        validators.EqualTo('password', message='Passwords must match'),
        validators.DataRequired()
    ])


app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='This key must be secret!',
    WTF_CSRF_ENABLED=False,
)

@app.route('/locales', methods = ['GET'])
def locales():
    return jsonify(['ru', 'en', 'it'])

@app.route('/meta', methods = ['GET'])
def meta():
    now = datetime.datetime.now()
    meta_data = {
        'current_date': now.strftime('%Y-%m-%d'),
        'current_time': now.strftime('%H:%M'),
        'received_headers': dict(request.headers),
        'received_query_args': dict(request.args)
    }
    return jsonify(meta_data)

@app.route('/form/user', methods = ['POST'])
def form_user():
    form = LoginForm(request.form)

    if form.validate():
        status = 0
        errors = []
    else:
        status = 1
        errors = form.errors

    return jsonify({
        "status": status,
        "errors": errors
        })

@app.route('/server/<path:filename>', methods = ['GET'])
def server(filename):
    script_dir = os.path.dirname(__file__)
    rel_path = 'files/'
    abs_file_path = os.path.join(script_dir, rel_path, filename)
    try:
        with open(abs_file_path, 'r') as f:
            return f.read()
    except IOError:
        return "Error", 404

if __name__ == '__main__':
    app.run()