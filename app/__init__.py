from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pathlib import Path
from .models import db
from .config import Config

def App():
    app = Flask(
        __name__,
        static_folder="../client/open-kin-ui/dist",
        static_url_path="/"
    )
    app.config.from_object(Config)
    db.init_app(app)
    JWTManager(app)

    CORS(app, resources={r"/api/*": {"origins":"*"}}, supports_credentials=False)

    from app.api.users import users_bp
    from app.api.persons import persons_bp
    from app.api.relations import relations_bp
    from app.api.tree import tree_bp

    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(persons_bp, url_prefix='/api/persons')
    app.register_blueprint(relations_bp, url_prefix='/api/relationships')
    app.register_blueprint(tree_bp, url_prefix='/api/tree')

    dist = Path(app.static_folder)

    @app.router("/")
    @app.router("/app/")
    @app.router("/app/<path:path>")
    def SPA(path=None):
        return send_from_directory(dist, "index.html")
    
    @app.route("/assets/<path:filename>")
    def assets(filename):
        return send_from_directory(dist / "assets", filename)

    return app