import json
from time import time
from os.path import join as join_path

import requests
import concurrent.futures

# example asset API usage
# assets_json = get_audio_assets(app.config['PREDIX_AUTH'])
# audio_file_paths = get_audio_for_assets(
#       app.config['PREDIX_AUTH'], assets_json)


SAFETY_ASSET_LIST_URL = ('https://ie-public-safety.run.aws-usw02-pr.ice.'
                         'predix.io/v1/assets/search?{query}')
PEDESTRIAN_ASSET_URL = ('https://ie-pedestrian.run.aws-usw02-pr.ice.predix.io/'
                        'v1/assets/search?{query}')


DEFAULT_BBOX = (33.235775, -118.031017, 32.290782, -116.414807, )

TYPE_AUDIO = 'media-type=AUDIO'
TYPE_EVENT_PEDESTRIAN = 'event-types=SFIN,SFOUT'


def _parse_location(loc):
    latlng = loc.split(',')
    return {'lat': latlng[0], 'lng': latlng[1]}


def _format_bbox(bbox):
    return ('{top_left_lat}:{top_left_lng},'
            '{bot_right_lat}:{bot_right_lng}').format(
                top_left_lat=bbox[0],
                top_left_lng=bbox[1],
                bot_right_lat=bbox[2],
                bot_right_lng=bbox[3])


def get_assets(auth,
               asset_url,
               media_type='',
               event_type='',
               bbox=DEFAULT_BBOX):
    params = {
        'bbox': _format_bbox(bbox)
    }
    asset_query_url = asset_url.format(
        query='&'.join((media_type, event_type,)))
    rsp = requests.get(asset_query_url, params=params, auth=auth)

    return rsp.text


def get_audio_assets(auth, bbox=DEFAULT_BBOX):
    assets_json = get_assets(auth,
                             SAFETY_ASSET_LIST_URL,
                             media_type=TYPE_AUDIO,
                             bbox=bbox)
    return assets_json


def get_pedestrian_event_assets(auth, bbox=DEFAULT_BBOX):
    assets_json = get_assets(auth,
                             PEDESTRIAN_ASSET_URL,
                             event_type=TYPE_EVENT_PEDESTRIAN,
                             bbox=bbox)
    return assets_json


def extract_data_from_assets(auth, assets_json, extractor_fn):
    assets = json.loads(assets_json)['_embedded']['assets']
    enriched_assets = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(extractor_fn, auth, asset)
                   for asset in assets]
        for future in concurrent.futures.as_completed(futures):
            try:
                updated_asset = future.result()
                enriched_assets.append(updated_asset)
            except (requests.exceptions.Timeout, ValueError):
                pass

    return enriched_assets


def get_pedestrians_for_assets(auth, assets_json):
    return extract_data_from_assets(auth, assets_json, get_pedestrian_numbers)


def get_audio_for_assets(auth, assets_json):
    return extract_data_from_assets(auth, assets_json,
                                    get_recent_audio_media_url)


def request_asset_data(auth, asset, query_url, start_ts, end_ts):
    asset_url = asset['_links']['self']['href'].replace('http', 'https')
    time_range_param = '&'.join(('start-ts={}'.format(start_ts),
                                 'end-ts={}'.format(end_ts),))
    url = '{base_url}/{query_url}&{params}'.format(
        base_url=asset_url, query_url=query_url, params=time_range_param)

    rsp = requests.get(url, auth=auth)
    if rsp.text:
        return json.loads(rsp.text)
    else:
        raise ValueError('Empty reply')


def get_recent_audio_media_url(auth, asset):
    # start_ts from 1h ago
    start_ts = (int(time()) - 3600) * 1000
    end_ts = int(time()) * 1000

    query_url = "media?&media-types=AUDIO"

    latest_asset = request_asset_data(auth, asset, query_url, start_ts,
                                      end_ts)['_embedded']['medias'][-1]

    return {asset['device-id']:
            {'audio_path': download_audio(auth, latest_asset),
             'location': _parse_location(asset['coordinates']['P1'])}}


def get_pedestrian_numbers(auth, asset, event_types='SFIN,SFOUT', size='100'):
    # start_ts from 0.5h ago
    start_ts = (int(time()) - 1800) * 1000
    end_ts = int(time()) * 1000

    query_url = ("events?event-types={event_types}&size={size}").format(
                       event_types=event_types,
                       size=size)
    ppl_events = request_asset_data(auth, asset, query_url, start_ts,
                                    end_ts)['_embedded']['events']
    return {asset['device-id']:
            {'pedestrians': get_avg_ppl(ppl_events),
             'location': _parse_location(asset['coordinates']['P1'])}}


def get_avg_ppl(ppl_events):
    total = sum(int(event['measures'][0]['value']) for event in ppl_events)
    return total / len(ppl_events)


def download_audio(auth, asset_dict, timeout=10):
    save_path = '/tmp'

    url = asset_dict['url'].replace('http', 'https')
    print 'Device id: {0}, url: {1}'.format(asset_dict['device-id'], url)
    local_fname = url.split('/')[-1]
    save_path = join_path(save_path, local_fname)
    rsp = requests.get(url, stream=True, auth=auth, timeout=timeout)
    with open(save_path, 'wb') as f:
        for chunk in rsp.iter_content(chunk_size=2048):
            if chunk:
                f.write(chunk)

    return save_path
