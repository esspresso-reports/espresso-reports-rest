from flask_restx import Namespace, fields

user_api = Namespace('user', description='access information about users')

user_dto = user_api.model('user', {
    'id': fields.String,
    'email': fields.String(required=True, description='the users email address'),
    'email_verified': fields.Boolean(required=True),
    'is_disabled': fields.Boolean(required=True)
})