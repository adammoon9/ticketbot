from typing import TYPE_CHECKING, override
from ..db import Base
from sqlalchemy import Boolean, ForeignKey, Index, Integer, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User
    from .event import Event

class Subscription(Base):
    __tablename__ = 'subscriptions'
    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', name='uq_subscriptions_user_event'),
        Index('index_subscription_event', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('1'))

    # relationships
    user: Mapped['User'] = relationship('User', back_populates='subscriptions', foreign_keys=user_id)
    event: Mapped['Event'] = relationship('Event', back_populates='subscriptions', foreign_keys=event_id)

    @override
    def __repr__(self) -> str:
        return f'<Subscription> user={self.user_id} event={self.event_id}, active={self.active}'
