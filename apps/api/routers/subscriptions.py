from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from pydantic import BaseModel
from ..db import get_session
from ..models.user import User
from ..models.event import Event
from ..models.subscription import Subscription
from ..schemas import SubscriptionCreate, SubscriptionResponse


class Message(BaseModel):
    message: str


router = APIRouter()


@router.get(
    "",
    response_model=list[SubscriptionResponse],
    responses={404: {"model": Message}},
    status_code=HTTP_200_OK,
)
def get_subscriptions_all(db: Session = Depends(get_session)):
    subscriptions = db.query(Subscription).all()
    if not subscriptions:
        raise HTTPException(status_code=404, detail="No subscriptions found.")
    
    return subscriptions


@router.post("", response_model=SubscriptionResponse, status_code=HTTP_201_CREATED)
def create_subscription(
    payload: SubscriptionCreate, response: Response, db: Session = Depends(get_session)
):
    user = db.query(User).filter_by(email=payload.email).one_or_none()
    if not user:
        user = User(email=payload.email)
        db.add(user)
        db.flush()

    event = db.query(Event).filter_by(url=payload.event_url).one_or_none()
    if not event:
        event = Event(url=payload.event_url)
        db.add(event)
        db.flush()

    subscription = Subscription(user_id=user.id, event_id=event.id, active=True)
    db.add(subscription)
    created = True
    try:
        db.commit()
        db.refresh(subscription)
    except IntegrityError:
        db.rollback()
        subscription = (
            db.query(Subscription).filter_by(user_id=user.id, event_id=event.id).one()
        )
        created = False
    db.refresh(subscription)

    response.status_code = HTTP_201_CREATED if created else HTTP_200_OK
    return subscription


@router.get(
    "/{id}",
    response_model=SubscriptionResponse,
    responses={404: {"model": Message}},
    status_code=HTTP_200_OK,
)
def get_subscription(id: int, db: Session = Depends(get_session)):
    subscription = db.query(Subscription).filter_by(id=id).one_or_none()
    if not subscription:
        raise HTTPException(
            status_code=404, detail=f"Subscription not found with id: {id}"
        )

    return subscription


@router.delete(
    "/{id}", responses={404: {"model": Message}}, status_code=HTTP_204_NO_CONTENT
)
def delete_subscription(id: int, db: Session = Depends(get_session)):
    subscription = db.query(Subscription).filter_by(id=id).one_or_none()
    if not subscription:
        raise HTTPException(
            status_code=404, detail=f"Subscription not found with id: {id}"
        )

    db.delete(subscription)
    db.commit()
    return


@router.patch(
    "/{id}/flip_status", responses={404: {"model": Message}}, status_code=HTTP_200_OK
)
def flip_subscription_status(id: int, db: Session = Depends(get_session)):
    subscription = db.query(Subscription).filter_by(id=id).one_or_none()
    if not subscription:
        raise HTTPException(
            status_code=404, detail=f"Subscription not found with id: {id}"
        )

    subscription.active = not subscription.active
    db.commit()
    db.refresh(subscription)
    return subscription
