#! ../env/bin/python
# -*- coding: utf-8 -*-

__author__ = 'bl0ckstar'
__email__ = 'bl0ckstar@protonmail.com'
__version__ = '1.3'

from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache
from flask_migrate import Migrate
from webassets.loaders import PythonLoader as PythonAssetsLoader

from flaskblog.controllers.main import main
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.errors.handlers import errors

from flaskblog import assets
from flaskblog.models import db
#from flaskblog import settings

from flaskblog.extensions import (
#    cache,
    assets_env,
    debug_toolbar,
    login_manager,
    mail
)

load_dotenv()

def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. flaskblog.settings.ProdConfig

        env:   The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    #app.config.from_pyfile('settings.py')
    app.config.from_object(object_name)

    # initialize the cache
    cache = Cache(app, config={"CACHE_TYPE": app.config.get('CACHE_TYPE')})
    cache.init_app(app)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # initialize SQLAlchemy
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)

    login_manager.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    # register our blueprints
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    #init mailserver

    mail.init_app(app)

    return app
