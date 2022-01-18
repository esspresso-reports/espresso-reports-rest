import requests
from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.oauth2.rfc7662 import IntrospectTokenValidator
from flask import current_app


class EspressoIntrospectTokenValidator(IntrospectTokenValidator):
    def introspect_token(self, token_string):
        url = current_app.config.get('ESPRESSO_IDP_INTROSPECT_URL')
        data = {'token': token_string, 'token_type_hint': 'access_token'}
        auth = (current_app.config.get('ESPRESSO_KC_CLIENT_ID'), current_app.config.get('ESPRESSO_KC_CLIENT_SECRET'))
        resp = requests.post(url, data=data, auth=auth)
        resp.raise_for_status()
        return resp.json()


require_oauth = ResourceProtector()
require_oauth.register_token_validator(EspressoIntrospectTokenValidator())
