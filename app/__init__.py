from flask import Flask
from .config import Config
from .models.postgres_models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .routes import api
    app.register_blueprint(api.bp)

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app