# ticketbot
A tool to check availability of concert tickets on TicketMaster

## Run the app in dev
```
uvicorn apps.api.main:app --reload
```

## Simple alembic migration
```bash
alembic init migrations
```
edit `alembic.ini` and change database_url = sqlite:///ticketbot.db

then edit `migrations/env.py`
```python
from apps.api.db import engine, Base
target_metadata = Base.metadata
```
Finally run
```bash
alembic revision --autogenerate -m 'initial'
alembic upgrade head
```
