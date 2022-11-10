from pathlib import Path
from typing import Tuple

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from twitchAPI.oauth import refresh_access_token


class Client:
    _twitch: Twitch
    _tokens: dict
    client_id: str
    client_secret: str
    SCOPES = [AuthScope.CHANNEL_READ_REDEMPTIONS]

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def twitch(self) -> Twitch:
        if getattr(self, '_twitch', None) is None:
            self._twitch = Twitch(self.client_id, self.client_secret)
            self._twitch.set_user_authentication(self.SCOPES, **self.load_tokens())
        return self._twitch

    @property
    def tokens(self) -> dict:
        if getattr(self, '_tokens', None) is None:
            self._tokens = self.load_tokens()
        return self._tokens

    def load_tokens(self) -> dict:
        token_cache = Path(Path.home(), '.chicken-hat')
        if not token_cache.exists():
            token, refresh_token = self.authenticate()
            token_cache.write_text(refresh_token)
        else:
            token, refresh_token = refresh_access_token(
                token_cache.read_text(), self.client_id, self.client_secret
            )
        return {'token': token, 'refresh_token': refresh_token}

    def authenticate(self) -> Tuple[str, str]:
        auth = UserAuthenticator(self._twitch, self.SCOPES, force_verify=False)
        return auth.authenticate()
