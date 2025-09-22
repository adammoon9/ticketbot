from flask_restx import Namespace, fields

def get_subscription_model(ns: Namespace):
    return ns.model('Subscription', {
        'id': fields.Integer(readOnly=True),
        'user_id': fields.Integer(required=True),
        'event_id': fields.Integer(required=True),
        'active': fields.Boolean(required=True, default=False),
    })
