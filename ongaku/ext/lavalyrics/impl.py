from __future__ import annotations

import typing

from . import abc as abc_

__all__ = (
    "Lyrics",
    "LyricLine",
)


class Lyrics(abc_.Lyrics):
    def __init__(
        self,
        *,
        source_name: str,
        provider: str,
        text: str | None,
        lines: typing.Sequence[abc_.LyricLine],
        plugin: typing.Mapping[str, typing.Any],
    ) -> None:
        self._source_name = source_name
        self._provider = provider
        self._text = text
        self._lines = lines
        self._plugin = plugin


class LyricLine(abc_.LyricLine):
    def __init__(
        self,
        *,
        timestamp: int,
        duration: int,
        line: str,
        plugin: typing.Mapping[str, typing.Any],
    ) -> None:
        self._timestamp = timestamp
        self._duration = duration
        self._line = line
        self._plugin = plugin
