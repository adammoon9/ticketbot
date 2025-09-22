from flask_restx import Namespace, Resource, reqparse
from flask_restx._http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from ..resources.subscription_model import get_subscription_model
from ..models.subscription import Subscription
from ..models.user import User
from ..models.event import Event
from ..extensions import db

ns = Namespace('subscriptions', description='Subscription Operations')
subscription_model = get_subscription_model(ns)

parser = reqparse.RequestParser()
parser.add_argument('email', type=int, required=True)
parser.add_argument('event_url', type=int, required=True)

@ns.route('/')
class SubscriptionList(Resource):
    @ns.doc('get_subscriptions')
    @ns.marshal_list_with(subscription_model)
    @ns.response(code=404, description='No subscriptions found.')
    def get(self):
        subscriptions = Subscription.query.all()
        if subscriptions:
            return subscriptions

        ns.abort(HTTPStatus.BAD_REQUEST, message='No subscriptions found')

    @ns.doc('add_subscription')
    @ns.expect(subscription_model)
    @ns.marshal_with(subscription_model, code=HTTPStatus.CREATED)
    def post(self):
        args = parser.parse_args()
        # Check input arguments
        email = args.get('email')
        url = args.get('event_url')
        if not (url or email):
            ns.abort(HTTPStatus.BAD_REQUEST, message='Required field not filled, check and try again')

        # Check user and event exist in database, if not create them
        try:
            user = User.query.filter_by(email=email).one_or_none()
            if not user:
                user = User(email=email)
                db.session.add(new_user)
                db.session.flush()

            event = Event.query.filter_by(url=url).one_or_none()
            if not event:
                event = Event(url=url)
                db.session.add(new_event)
                db.session.flush()

            # Make sure the subscription doesn't exist already:
            subscription = Subscription.query.filter_by(user_id=user.id, event_id=event.id).first()
            created = False
            if not subscription:
                subscription = Subscription(user_id=user.id, event_id=event.id, active=True)
                db.session.add(subscription)
                db.session.flush()
                created = True

            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            subscription = Subscription.query.filter_by(user_id=user.id, event_id=event.id).first()
            if not subscription:
                ns.abort(HTTPStatus.CONFLICT, message='Conflict retry')

            created = False

        status = HTTPStatus.CREATED if created else HTTPStatus.OK

        return subscription, status

@ns.route('/<id>')
@ns.param('id', 'Subscription ID')
@ns.response(HTTPStatus.NOT_FOUND, 'Subscription not found')
class SubscriptionID(Resource):
    @ns.doc('get_subscription')
    @ns.marshal_with(subscription_model)
    def get(self, id:int):
        subscription = Subscription.query.filter_by(id=id).one_or_none()
        if subscription:
            return subscription, HTTPStatus.OK

        ns.abort(HTTPStatus.NOT_FOUND, message=f'Subscription not found with id: {id}')

    @ns.doc('delete_subscription')
    @ns.marshal_with(subscription_model)
    def delete(self, id:int):
        subscription = Subscription.query.filter_by(id=id).one_or_none()
        if subscription:
            db.session.delete(subscription)
            db.session.commit()
            return '', HTTPStatus.NO_CONTENT

        ns.abort(HTTPStatus.NOT_FOUND, message=f'Subscription not found with id: {id}')
