import datetime
from typing import override, TYPE_CHECKING
from ..db import Base
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .subscription import Subscription

class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    last_checked_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now())
    next_checked_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now())

    # relationships
    subscriptions: Mapped[list['Subscription']] = relationship(
        'Subscription',
        back_populates='event',
        cascade='all, delete-orphan'
    )

    @override
    def __repr__(self) -> str:
        return f'<Event> {self.url} id={self.id}'
