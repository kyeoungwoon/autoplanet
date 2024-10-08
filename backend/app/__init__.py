from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import main
    from .api import api

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')

    return app