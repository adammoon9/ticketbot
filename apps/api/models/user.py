from typing import override, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import Base

if TYPE_CHECKING:
    from .subscription import Subscription

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    # password: Mapped[str] = mapped_column(String, nullable=False)

    # relationships
    subscriptions: Mapped[list['Subscription']] = relationship(
        'Subscription',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    @override
    def __repr__(self) -> str:
        return f'<User> {self.email}'
