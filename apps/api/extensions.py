from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title="Ticketmaster Bot Subscriptions API",
    version="0.1",
    description="API for creating subscriptions to the ticketmaster bot."
)
