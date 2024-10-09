import typing

import hikari

import ongaku
from ongaku import Client
from ongaku import Session
from ongaku.ext.lavalyrics import impl
from ongaku.ext.lavalyrics.abc import LyricLine
from ongaku.ext.lavalyrics.abc import Lyrics

__all__ = ("LavaLyricsExtension",)


class LavaLyricsExtension(ongaku.Extension):
    def __init__(self, client: Client) -> None:
        super().__init__(client)

    def event_handler(self, payload: typing.Mapping[str, typing.Any], session: Session) -> ongaku.OngakuEvent | None:
        return None

    def _build_lyric_line(self, payload: typing.Mapping[str, typing.Any]) -> LyricLine:
        return impl.LyricLine(
            timestamp=payload["timestamp"],
            duration=payload["duration"],
            line=payload["line"],
            plugin=payload["plugin"],
        )

    def _build_lyrics(self, payload: typing.Mapping[str, typing.Any]) -> Lyrics:
        lines: typing.Sequence[LyricLine] = []

        for lyric in payload["lines"]:
            lines.append(self._build_lyric_line(lyric))

        return impl.Lyrics(
            source_name=payload["sourceName"],
            provider=payload["provider"],
            text=payload["text"],
            lines=lines,
            plugin=payload["plugin"],
        )

    async def fetch_lyrics_from_playing(
        self,
        session_id: str,
        guild: hikari.SnowflakeishOr[hikari.PartialGuild],
        /,
        *,
        skip_track_source: bool = False,
        session: Session | None = None,
    ) -> Lyrics | None:
        """Fetch Lyrics From Playing.

        Fetch the lyrics from a player that is currently playing a track.

        Parameters
        ----------
        session_id
            The session id attached to the player.
        guild
            The guild or guild id the player is in.
        skip_track_source
            Whether to skip the tracks source for lyrics or not.
        session
            The session to use to fetch information from.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the players could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Lyrics
            If successfully found, a [Lyrics][ongaku.ext.lavalyrics.abc.Lyrics] object.
        None
            If the lyrics do not exist for the track, or if the track requested does not exist.
        """
        if not session:
            session = self.client.session_handler.fetch_session()

        try:
            response = await session.request(
                "GET",
                "/sessions/{session_id}/players/{guild_id}/track/lyrics".format(
                    session_id=session_id, guild_id=hikari.Snowflake(guild)
                ),
                dict,
                params={"skipTrackSource": skip_track_source},
            )
        except ongaku.RestEmptyError:
            return None

        if response is None:
            raise ValueError("Response is required for this request.")

        return self._build_lyrics(response)

    async def fetch_lyrics(
        self,
        track: ongaku.Track | str,
        /,
        *,
        skip_track_source: bool = False,
        session: Session | None = None,
    ) -> Lyrics | None:
        """Fetch Lyrics.

        Fetch the lyrics of a specified track, or its encoded value.

        Parameters
        ----------
        track
            The track you wish to fetch the lyrics for.
        skip_track_source
            Whether to skip the tracks source for lyrics or not.
        session
            The session to use to fetch information from.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the players could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Lyrics
            If successfully found, a [Lyrics][ongaku.ext.lavalyrics.abc.Lyrics] object.
        None
            If the lyrics do not exist for the track, or if the track requested does not exist.
        """
        if not session:
            session = self.client.session_handler.fetch_session()

        if isinstance(track, ongaku.Track):
            track = track.encoded

        try:
            response = await session.request(
                "GET",
                "/lyrics",
                dict,
                params={"track": track, "skipTrackSource": skip_track_source},
            )
        except ongaku.RestEmptyError:
            return None

        if response is None:
            raise ValueError("Response is required for this request.")

        return self._build_lyrics(response)
