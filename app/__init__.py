from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    from app.routes import bp
    app.register_blueprint(bp)
    
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            # Table already exists (race condition with multiple workers)
            pass
    
    return app
