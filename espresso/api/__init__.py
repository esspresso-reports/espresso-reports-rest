from flask import Blueprint
from flask_restx import Api

from espresso.api.user.api import user_api
from espresso.api.report.api import report_api

blueprint = Blueprint('espresso api', __name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-token'
    }
}

api = Api(
    blueprint,
    authorizations=authorizations
)

api.add_namespace(user_api)
api.add_namespace(report_api)
