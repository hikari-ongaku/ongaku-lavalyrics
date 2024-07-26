from __future__ import annotations

import typing

import hikari
import mock
import pytest

import ongaku
from ongaku.ext.lavalyrics.extension import Extension

if typing.TYPE_CHECKING:
    from ongaku import Client

PayloadT: typing.TypeAlias = typing.Final[typing.Mapping[str, typing.Any]]

LYRICS_LINE_PAYLOAD: PayloadT = {
    "timestamp": 1,
    "duration": 2,
    "line": "line",
    "plugin": {},
}

LYRICS_PAYLOAD: PayloadT = {
    "sourceName": "source_name",
    "provider": "provider",
    "text": "text",
    "lines": [LYRICS_LINE_PAYLOAD],
    "plugin": {},
}


def test__build_lyrics():
    ext = Extension(mock.Mock())

    lyrics = ext._build_lyrics(LYRICS_PAYLOAD)

    assert lyrics.source_name == "source_name"
    assert lyrics.provider == "provider"
    assert lyrics.text == "text"
    assert lyrics.lines == [ext._build_lyric_line(LYRICS_LINE_PAYLOAD)]
    assert lyrics.plugin == {}


def test__build_lyric_line():
    ext = Extension(mock.Mock())

    line = ext._build_lyric_line(LYRICS_LINE_PAYLOAD)
    assert line.timestamp == 1
    assert line.duration == 2
    assert line.line == "line"
    assert line.plugin == {}


@pytest.mark.asyncio
async def test_fetch_lyrics_with_track():
    client: Client = mock.Mock()
    ext = Extension(client)

    session = mock.AsyncMock()

    track: ongaku.Track = mock.MagicMock(spec=ongaku.Track)

    track.encoded = "encoded"

    with (
        mock.patch.object(
            client.session_handler, "fetch_session", return_value=session
        ) as patched_fetch_session,
        mock.patch.object(
            session, "request", return_value=mock.AsyncMock()
        ) as patched_request,
    ):
        await ext.fetch_lyrics(track)

        patched_fetch_session.assert_called_once()

        patched_request.assert_called_once_with(
            "GET",
            "/lyrics",
            dict,
            params={"track": "encoded", "skipTrackSource": False},
        )


@pytest.mark.asyncio
async def test_fetch_lyrics_track_source():
    client: Client = mock.Mock()
    ext = Extension(client)

    session = mock.AsyncMock()

    with (
        mock.patch.object(
            client.session_handler, "fetch_session", return_value=session
        ) as patched_fetch_session,
        mock.patch.object(
            session, "request", return_value=mock.AsyncMock()
        ) as patched_request,
    ):
        await ext.fetch_lyrics("encoded", skip_track_source=True)

        patched_fetch_session.assert_called_once()

        patched_request.assert_called_once_with(
            "GET", "/lyrics", dict, params={"track": "encoded", "skipTrackSource": True}
        )


@pytest.mark.asyncio
async def test_fetch_lyrics():
    client: Client = mock.Mock()
    ext = Extension(client)

    session = mock.AsyncMock()

    with (
        mock.patch.object(
            client.session_handler, "fetch_session", return_value=session
        ) as patched_fetch_session,
        mock.patch.object(
            session, "request", return_value=mock.AsyncMock()
        ) as patched_request,
    ):
        await ext.fetch_lyrics("encoded")

        patched_fetch_session.assert_called_once()

        patched_request.assert_called_once_with(
            "GET",
            "/lyrics",
            dict,
            params={"track": "encoded", "skipTrackSource": False},
        )


@pytest.mark.asyncio
async def test_fetch_lyrics_from_playing_track_source():
    client: Client = mock.Mock()
    ext = Extension(client)

    session = mock.AsyncMock()

    with (
        mock.patch.object(
            client.session_handler, "fetch_session", return_value=session
        ) as patched_fetch_session,
        mock.patch.object(
            session, "request", return_value=mock.AsyncMock()
        ) as patched_request,
    ):
        await ext.fetch_lyrics_from_playing(
            "session_id", hikari.Snowflake(1234), skip_track_source=True
        )

        patched_fetch_session.assert_called_once()

        patched_request.assert_called_once_with(
            "GET",
            "/sessions/session_id/players/1234/track/lyrics",
            dict,
            params={"skipTrackSource": True},
        )


@pytest.mark.asyncio
async def test_fetch_lyrics_from_playing():
    client: Client = mock.Mock()
    ext = Extension(client)

    session = mock.AsyncMock()

    with (
        mock.patch.object(
            client.session_handler, "fetch_session", return_value=session
        ) as patched_fetch_session,
        mock.patch.object(
            session, "request", return_value=mock.AsyncMock()
        ) as patched_request,
    ):
        await ext.fetch_lyrics_from_playing("session_id", hikari.Snowflake(1234))

        patched_fetch_session.assert_called_once()

        patched_request.assert_called_once_with(
            "GET",
            "/sessions/session_id/players/1234/track/lyrics",
            dict,
            params={"skipTrackSource": False},
        )
