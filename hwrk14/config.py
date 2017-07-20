# -*- coding: utf-8 -*-


DEBUG = True
SECRET_KEY = 'The secret key so secret that its unauthorized disclosure might cause serious damage to national security'

# Database settings:
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = False