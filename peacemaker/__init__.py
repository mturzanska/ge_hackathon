from flask import Flask

from api.conf import settings
from api.auth import AuthenticatorFactory

safety_auth_settings = settings.copy()
safety_auth_settings.pop('pedestrian_event_zone_id')
safety_auth_settings['zone_id'] = safety_auth_settings.pop(
    'public_safety_zone_id')

pedestrian_auth_settings = settings.copy()
pedestrian_auth_settings.pop('public_safety_zone_id')
pedestrian_auth_settings['zone_id'] = pedestrian_auth_settings.pop(
    'pedestrian_event_zone_id')


safety_auth_factory = AuthenticatorFactory(**safety_auth_settings)
safety_auth_factory.set_token()
safety_authenticator = safety_auth_factory.create_authenticator()

pedestrian_auth_factory = AuthenticatorFactory(**pedestrian_auth_settings)
pedestrian_auth_factory.set_token()
pedestrian_authenticator = pedestrian_auth_factory.create_authenticator()


app = Flask(__name__)
app.config['SAFETY_AUTH'] = safety_authenticator
app.config['PEDESTRIAN_AUTH'] = pedestrian_authenticator

from peacemaker import views
