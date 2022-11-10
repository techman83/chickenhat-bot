from uuid import UUID
import os

from twitchAPI.pubsub import PubSub

from .auth import Client


def callback_channel(uuid: UUID, data: dict) -> None:
    print('got callback for UUID ' + str(uuid))
    print(data)


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
