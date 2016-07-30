from flask import Flask

from api.conf import settings
from api.auth import AuthenticatorFactory

auth_factory = AuthenticatorFactory(**settings)
auth_factory.set_token()
authenticator = auth_factory.create_authenticator()

app = Flask(__name__)
app.config['PREDIX_AUTH'] = authenticator

from peacemaker import views
