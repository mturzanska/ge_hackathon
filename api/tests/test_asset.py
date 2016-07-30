import json


from unittest import TestCase, skip
from mock import MagicMock, patch

from api.asset import get_assets, get_audio_for_assets, download_audio


class TestGetAllAssets(TestCase):
    def setUp(self):
        self.auth = lambda x: x
        self.mock_rsp = MagicMock()
        type(self.mock_rsp).status_code = 200
        type(self.mock_rsp).text = '{"json": "true"}'

    @patch('requests.get')
    def test_correct_params(self, mock_get):
        mock_get.return_value = self.mock_rsp
        get_assets(self.auth, 'asset-url')
        _, kwargs = mock_get.call_args
        params = kwargs['params']

        self.assertIn('bbox', params)
        self.assertRegexpMatches(params['bbox'],
                                 r'^[\d.-]+:[\d.-]+,[\d.-]+:[\d.-]+')


class TestGetAudio(TestCase):
    def setUp(self):
        self.auth = lambda x: x
        self.assets = [
            {
                'timestamp': '000000000',
                'device-id': 'PYH4010-57',
                'url': ('http://ie-media-service-dev.run.aws-usw02-pr.'
                        'ice.predix.io/media/file/1000000023_1457390757339_AUDIO'
                        )
            }, {
                'timestamp': '123123123',
                'device-id': 'HYP1040-75',
                'url': ('http://ie-media-service-dev.run.aws-usw02-pr.'
                        'ice.predix.io/media/file/1000000022_1457390757339_AUDIO')
            }
        ]
        self.assets_json = json.dumps(self.assets)

    @skip('')
    @patch('requests.get')
    def test_get_audio_for_assets(self, mock_get):
        with patch('api.asset.download_audio') as mock_download:
            get_audio_for_assets(self.auth, self.assets_json)
            _, kwargs = mock_get.call_args
            mock_download.assert_called_with(self.assets[-1]['url'])

    @patch('requests.get')
    def test_download_audio(self, mock_get):
        asset = self.assets[-1]
        path = download_audio(self.auth, asset, timeout=10)
        expected_url = self.assets[-1]['url'].replace('http', 'https')
        mock_get.assert_called_with(expected_url,
                                    auth=self.auth,
                                    stream=True,
                                    timeout=10)
        self.assertEqual(path, '/tmp/1000000022_1457390757339_AUDIO')
