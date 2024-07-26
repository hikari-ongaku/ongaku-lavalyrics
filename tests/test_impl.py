from __future__ import annotations

from ongaku.ext.lavalyrics.impl import LyricLine
from ongaku.ext.lavalyrics.impl import Lyrics


def test_lyrics():
    line = LyricLine(timestamp=1, duration=2, line="line", plugin={})
    lyrics = Lyrics(
        source_name="source_name",
        provider="provider",
        text="text",
        lines=[line],
        plugin={},
    )

    assert lyrics.source_name == "source_name"
    assert lyrics.provider == "provider"
    assert lyrics.text == "text"
    assert lyrics.lines == [line]
    assert lyrics.plugin == {}


def test_lyric_line():
    line = LyricLine(timestamp=1, duration=2, line="line", plugin={})

    assert line.timestamp == 1
    assert line.duration == 2
    assert line.line == "line"
    assert line.plugin == {}
