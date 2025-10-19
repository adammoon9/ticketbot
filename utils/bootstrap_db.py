from apps.api.db import Base, engine
from apps.api.models import user, event, subscription

Base.metadata.create_all(bind=engine)
