"""
SAPO OAuth support.

This adds support for SAPO OAuth service. An application must
be registered first on twitter and the settings SAPO_CONSUMER_KEY
and SAPO_CONSUMER_SECRET must be defined with they corresponding
values.

User screen name is used to generate username.

By default account id is stored in extra_data field, check OAuthBackend
class for details on how to extend it.
"""
from django.utils import simplejson

from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, USERNAME


# Sapo configuration
SAPO_SERVER = 'id.sapo.pt'
SAPO_REQUEST_TOKEN_URL = 'https://%s/oauth/request_token' % SAPO_SERVER
SAPO_ACCESS_TOKEN_URL = 'https://%s/oauth/access_token' % SAPO_SERVER
# Note: oauth/authorize forces the user to authorize every time.
#       oauth/authenticate uses their previous selection, barring revocation.
SAPO_AUTHORIZATION_URL = 'http://%s/oauth/authenticate' % SAPO_SERVER
SAPO_CHECK_AUTH = 'https://services.sapo.pt/SSO/GetPublicProfile'


class SapoBackend(OAuthBackend):
    """Sapo OAuth authentication backend"""
    name = 'sapo'
    EXTRA_DATA = [('id', 'id')]

    def get_user_details(self, response):
        """Return user details from Sapo account"""
        return {USERNAME: response['screen_name'],
                'email': '',  # not supplied
                'fullname': response['name'],
                'first_name': response['name'],
                'last_name': ''}


class SapoAuth(ConsumerBasedOAuth):
    """Sapo OAuth authentication mechanism"""
    AUTHORIZATION_URL = SAPO_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = SAPO_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = SAPO_ACCESS_TOKEN_URL
    SERVER_URL = SAPO_SERVER
    AUTH_BACKEND = SapoBackend
    SETTINGS_KEY_NAME = 'SAPO_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'SAPO_CONSUMER_SECRET'

    def user_data(self, access_token):
        """Return user data provided"""
        request = self.oauth_request(access_token, SAPO_CHECK_AUTH)
        json = self.fetch_response(request)
        try:
            return simplejson.loads(json)
        except simplejson.JSONDecodeError:
            return None


# Backend definition
BACKENDS = {
    'sapo': SapoAuth,
}
