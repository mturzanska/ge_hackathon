import json
from os.path import join as join_path

import requests
import concurrent.futures

ASSET_LIST_URL = ('https://ie-public-safety.run.aws-usw02-pr.ice.predix.io'
                  '/v1/assets/search')


def _format_bbox(bbox):
    return ('{top_left_lat}:{top_left_lng},'
            '{bot_right_lat}:{bot_right_lng}').format(
                top_left_lat=bbox[0],
                top_left_lng=bbox[1],
                bot_right_lat=bbox[2],
                bot_right_lng=bbox[3])


def get_assets(auth, bbox=(33.235775, -118.031017, 32.290782, -116.414807,)):
    params = {
        'bbox': _format_bbox(bbox)
    }
    rsp = requests.get(ASSET_LIST_URL, params=params, auth=auth)

    return rsp.text


def get_audio_for_assets(auth, assets_json):
    assets = json.loads(assets_json)
    enriched_assets = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_audio, auth, asset, 10)
                   for asset in assets]
        for future in concurrent.futures.as_completed(futures):
            try:
                updated_asset = future.result()
                enriched_assets.append(updated_asset)
            except requests.exceptions.Timeout:
                pass

    return assets


def download_audio(auth, asset_dict, timeout=10):
    save_path = '/tmp'
    url = asset_dict.get('url')
    local_fname = url.split('/')[-1]
    save_path = join_path(save_path, local_fname)
    rsp = requests.get(url, stream=True, auth=auth, timeout=timeout)
    with open(save_path, 'wb') as f:
        for chunk in rsp.iter_content(chunk_size=2048):
            if chunk:
                f.write(chunk)

    return save_path
