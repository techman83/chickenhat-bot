import asyncio
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from twitchAPI.oauth import UserAuthenticator, refresh_access_token
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope


class Client:
    _twitch: Optional[Twitch] = None
    _tokens: Optional[Dict[str, str]] = None
    client_id: str
    client_secret: str
    SCOPES = [AuthScope.CHANNEL_READ_REDEMPTIONS]

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    async def get_twitch(self) -> Twitch:
        """Get an authenticated Twitch API instance"""
        if self._twitch is None:
            self._twitch = await Twitch(self.client_id, self.client_secret)
            tokens = await self.load_tokens()
            await self._twitch.set_user_authentication(
                tokens['token'], self.SCOPES, tokens['refresh_token']
            )
        return self._twitch

    async def load_tokens(self) -> Dict[str, str]:
        """Load or refresh authentication tokens"""
        if self._tokens is not None:
            return self._tokens

        token_cache = Path(Path.home(), '.chickenhat')
        if not token_cache.exists():
            token, refresh_token = await self.authenticate()
            token_cache.write_text(refresh_token)
        else:
            refresh_token = token_cache.read_text()
            token_data = await refresh_access_token(
                refresh_token, self.client_id, self.client_secret
            )
            token = token_data[0]
            refresh_token = token_data[1]

        self._tokens = {'token': token, 'refresh_token': refresh_token}
        return self._tokens

    async def authenticate(self) -> Tuple[str, str]:
        """Authenticate with Twitch and get tokens"""
        twitch = await Twitch(self.client_id, self.client_secret)
        auth = UserAuthenticator(twitch, self.SCOPES, force_verify=True)
        token, refresh_token = await auth.authenticate()
        return token, refresh_token
