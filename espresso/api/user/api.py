from authlib.integrations.flask_oauth2 import current_token
from flask import request, current_app
from flask_restx import Resource, reqparse

from espresso.api.user import user_api, user_dto
from espresso.api.user.service import update_user, delete_user, get_user_by_id, get_all_users, create_user, \
    update_user_settings, get_users_with_overdue_report
from espresso.api.auth import require_oauth


@user_api.route('/')
class UserListResource(Resource):
    @require_oauth('profile')
    @user_api.param('report_overdue', 'If set to True, only users with overdue reports are returned')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('report_overdue', type=bool)
        args = parser.parse_args()

        if current_app.config['ESPRESSO_ADMIN_ROLE'] not in current_token['resource_access']['espresso']['roles']:
            user_api.abort(401, "User is not authorized to view this resources")

        if args.get('report_overdue'):
            return get_users_with_overdue_report()
        return get_all_users()

    @require_oauth('profile')
    @user_api.expect(user_dto, validate=True)
    def post(self):
        new_user = request.json

        if 'espresso_admin' not in current_token['resource_access']['espresso']['roles']:
            user_api.abort(401, "User is not authorized to execute this operation")

        create_user(new_user)
        return 'user successfully created', 201

    @require_oauth('profile')
    @user_api.expect(user_dto, validate=True)
    def put(self):
        modified_user = request.json

        if modified_user['id'] != current_token['sub'] and \
                current_app.config['ESPRESSO_ADMIN_ROLE'] not in current_token['resource_access']['espresso']['roles']:
            user_api.abort(401, "User is not authorized to execute this operation")

        update_user(modified_user)
        return 'user successfully updated', 201


@user_api.route('/<user_id>')
@user_api.param('user_id', 'identifier of user')
class UserResource(Resource):

    @require_oauth('profile')
    @user_api.marshal_with(user_dto)
    def get(self, user_id):
        if current_token['sub'] != user_id or current_app.config['ESPRESSO_ADMIN_ROLE'] not in \
                current_token['resource_access']['espresso']['roles']:
            user_api.abort(401, "User is not authorized to view this resource")

        user = get_user_by_id(user_id)

        if not user:
            user_api.abort(404, "User not found")
        else:
            return 200, user

    @require_oauth('profile')
    def delete(self, user_id):
        if current_token['sub'] != user_id and current_app.config['ESPRESSO_ADMIN_ROLE'] not in \
                current_token['resource_access']['espresso']['roles']:
            user_api.abort(401, "User is not authorized to delete this resource")

        delete_user(user_id)
        return 204, 'user successfully deleted'


@user_api.route('/<user_id>/settings')
@user_api.param('user_id', 'The User identifier')
class UserResource(Resource):

    @require_oauth('profile')
    def get(self, user_id):
        if current_token['sub'] != user_id and current_app.config['ESPRESSO_ADMIN_ROLE'] not in \
                current_token['resource_access']['espresso']['roles']:
            user_api.abort(401, "User is not authorized to view this resource")

        user = get_user_by_id(user_id)

        if not user:
            user_api.abort(404, "User not found")
        else:
            return 200, user.settings

    @require_oauth('profile')
    @user_api.doc('update user settings')
    def post(self, user_id):
        if current_token['sub'] != user_id and current_app.config['ESPRESSO_ADMIN_ROLE'] not in \
                current_token['resource_access']['espresso']['roles']:
            user_api.abort(401, "User is not authorized to delete this resource")

        update_user_settings(user_id, request.json)
