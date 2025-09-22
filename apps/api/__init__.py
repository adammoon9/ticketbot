from .extensions import db, migrate, api
from .models.subscription import Subscription
from .models.event import Event
from .models.user import User
from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketbot.db'

    api.init_app(app)

    from .controllers.subscription_controller import ns as subscription_namespace
    api.add_namespace(subscription_namespace)

    db.init_app(app)
    migrate.init_app(app, db)

    return app
