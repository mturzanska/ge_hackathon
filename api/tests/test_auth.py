from unittest import TestCase
from mock import MagicMock, PropertyMock, patch

from requests.auth import AuthBase

from api.auth import AuthenticatorFactory, PredixAuth


class TestAuthenticatorFactorySetToken(TestCase):
    def setUp(self):
        self.factory = AuthenticatorFactory('client', 'zone', 'b64',
                                            'endpoint')
        self.mock_rsp = MagicMock()
        type(self.mock_rsp).status_code = 200
        type(self.mock_rsp).text = '{"access_token": "token!"}'

    @patch('requests.post')
    def test_sets_correct_headers(self, mock_post):
        mock_post.return_value = self.mock_rsp
        self.factory.set_token()
        _, kwargs = mock_post.call_args
        headers = kwargs['headers']

        self.assertIn('authorization', headers)
        self.assertIn('Content-Type', headers)
        self.assertEqual('Basic b64', headers['authorization'])
        self.assertEqual('application/x-www-form-urlencoded',
                         headers['Content-Type'])

    @patch('requests.post')
    def test_sets_correct_data(self, mock_post):
        mock_post.return_value = self.mock_rsp
        self.factory.set_token()
        _, kwargs = mock_post.call_args
        data = kwargs['data']

        self.assertIn('client_id', data)
        self.assertIn('grant_type', data)
        self.assertEqual('client', data['client_id'])

    @patch('requests.post')
    def test_sets_token_on_factory(self, mock_post):
        mock_post.return_value = self.mock_rsp
        self.factory.set_token()

        self.assertEqual(self.factory.token, 'token!')


class TestAuthenticatorFactoryCreateAuthenticator(TestCase):
    def setUp(self):
        self.factory = AuthenticatorFactory('client', 'zone', 'b64',
                                            'endpoint')
        self.mock_set_token = MagicMock()
        self.factory.set_token = self.mock_set_token

    def test_create_authenticator_when_token_none(self):
        self.factory.create_authenticator()

        self.assertTrue(self.mock_set_token.called)

    def test_create_authenticator_when_token_set(self):
        self.factory.token = 'token!'
        self.factory.create_authenticator()

        self.assertFalse(self.mock_set_token.called)

    def test_create_authenticator_create_authbase(self):
        auth = self.factory.create_authenticator()

        self.assertIsInstance(auth, AuthBase)


class TestPredixAuth(TestCase):
    def setUp(self):
        self.auth = PredixAuth('token!', 'zone!')
        self.request = MagicMock()

    def test_headers_set(self):
        self.request.headers = {}
        r = self.auth(self.request)
        self.assertIn('Authorization', r.headers)
        self.assertIn('predix-zone-id', r.headers)
        self.assertEqual('bearer token!', r.headers['Authorization'])
        self.assertEqual('zone!', r.headers['predix-zone-id'])
