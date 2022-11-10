import os
import logging
import requests
from requests.exceptions import RequestException
from uuid import UUID

from twitchAPI.pubsub import PubSub

from .auth import Client

OPENHAB_URL = os.environ.get('OPENHAB_URL')

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)-8s] %(message)s',
)


def launch_chickenhat():
    item_url = f'{OPENHAB_URL}/rest/items/ChickenHat'
    try:
        result = requests.post(
            item_url, data='ON', headers={'Content-Type': 'text/plain'}
        )
    except RequestException as exception:
        logging.error('Web request exception %s', exception)

    if result.status_code > 299:
        logging.error('Item update failed: %s (%s)', result.reason, result.status_code)
        logging.debug(result.text)
    else:
        logging.info('ChickenHat ON!')


def callback_channel(uuid: UUID, data: dict) -> None:
    logging.debug('Got callback for UUID %s', str(uuid))
    logging.debug(data)
    user = (
        data.get('data', {}).get('redemption', {}).get('user', {}).get('display_name')
    )
    title = (
        data.get('data', {}).get('redemption', {}).get('reward', {}).get('title', '')
    )
    if title.lower().replace(' ', '') == 'thechickenhat':
        logging.info('Chicken Hat Redeemed by %s!', user)
        launch_chickenhat()


def run_chicken_hat():
    twitch = Client(
        os.environ.get('TWITCH_CLIENT_ID', ''),
        os.environ.get('TWITCH_CLIENT_SECRET', ''),
    )
    pubsub = PubSub(twitch.twitch)
    pubsub.start()
    listener = pubsub.listen_channel_points('80751890', callback_channel)

    input('press ENTER to close...')

    pubsub.unlisten(listener)
    pubsub.stop()
