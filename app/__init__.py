from flask import Flask
from .models import db
from .config import Config

def App():
    app = Flask(__name__)
    app.config.from_object('Config')
    db.init_app(app)

    from app.api.users import users_bp
    from app.api.persons import persons_bp
    from app.api.relations import relations_bp

    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(persons_bp, url_prefix='/api/persons')
    app.register_blueprint(relations_bp, url_prefix='/api/relationships')

    return app