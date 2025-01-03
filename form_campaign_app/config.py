from flask import Flask, request
from form_campaign_app.setup import (
    constant as const,
)

import mimetypes
mimetypes.add_type('application/javascript', '.js')

import os

class Config:
    # Get the folder where this file is located
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Database configuration - changed to data.db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

def get_remote_address() -> str:
    """
    :return: the ip address for the current request
     (or 127.0.0.1 if none found)

    since request.remote_addr doesnt bypass proxied network
    we customized out own get_remote_address util
    """
    return request.access_route[-1] or "127.0.0.1"

app = Flask(__name__)
app.static_folder = const.APP_STATIC_FOLDER
app.config.from_object(Config)
