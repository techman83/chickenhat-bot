import asyncio
import logging
import os
import sys
from uuid import UUID

import requests
from requests.exceptions import RequestException
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.helper import first
from twitchAPI.type import CustomRewardRedemptionStatus

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
        return

    if result.status_code > 299:
        logging.error('Item update failed: %s (%s)', result.reason, result.status_code)
        logging.debug(result.text)
    else:
        logging.debug('ChickenHat ON!')


async def on_channel_points_redemption(data):
    """Handle channel points redemption events"""
    user = data.event.user_name
    reward_title = data.event.reward.title

    if reward_title.lower().replace(' ', '') == 'thechickenhat':
        logging.info('Chicken Hat Redeemed by %s!', user)
        launch_chickenhat()
    else:
        logging.info('%s Redeemed by %s!', reward_title, user)


async def run_chicken_hat_async():
    """Run the chicken hat bot with EventSub WebSocket"""
    # Check for required environment variables
    required_vars = ['TWITCH_CLIENT_ID', 'TWITCH_CLIENT_SECRET', 'TWITCH_USER_ID']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        logging.error(
            "Missing required environment variables: %s", ", ".join(missing_vars)
        )
        sys.exit(1)

    # Initialize the Twitch client
    twitch_client = Client(
        os.environ.get('TWITCH_CLIENT_ID', ''),
        os.environ.get('TWITCH_CLIENT_SECRET', ''),
    )

    # Get authenticated Twitch API instance
    twitch = await twitch_client.get_twitch()

    # Get user info
    user_id = os.environ.get('TWITCH_USER_ID', '')

    # Set up EventSub WebSocket
    event_sub = EventSubWebsocket(twitch)
    event_sub.start()

    # Subscribe to channel points redemption events
    await event_sub.listen_channel_points_custom_reward_redemption_add(
        broadcaster_user_id=user_id, callback=on_channel_points_redemption
    )

    logging.info('Chicken Hat Bot Started!')

    # Keep the bot running
    try:
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, asyncio.CancelledError):
        logging.info("Shutting down...")
    finally:
        event_sub.stop()
        await twitch.close()


def run_chicken_hat():
    """Entry point for the chicken hat bot"""
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_chicken_hat_async())
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    finally:
        loop.close()
