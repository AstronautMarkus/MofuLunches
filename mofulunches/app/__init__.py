from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
from .models.models import User, db

mail = Mail()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    mail.init_app(app)

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    
    return app