from __future__ import annotations

import typing

__all__ = ("LyricLine", "Lyrics")


class Lyrics:
    """Lyrics.

    A lyrics object.
    """

    __slots__: typing.Sequence[str] = (
        "_lines",
        "_plugin",
        "_provider",
        "_source_name",
        "_text",
    )

    @property
    def source_name(self) -> str:
        """The name of the source where the lyrics were fetched from."""
        return self._source_name

    @property
    def provider(self) -> str:
        """The name of the provider the lyrics was fetched from on the source."""
        return self._provider

    @property
    def text(self) -> str | None:
        """The lyrics text."""
        return self._text

    @property
    def lines(self) -> typing.Sequence[LyricLine]:
        """The lyrics lines."""
        return self._lines

    @property
    def plugin(self) -> typing.Mapping[str, typing.Any]:
        """Additional plugin specific data."""
        return self._plugin

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Lyrics):
            return False

        if self.source_name != other.source_name:
            return False

        if self.provider != other.provider:
            return False

        if self.text != other.text:
            return False

        if self.lines != other.lines:
            return False

        return self.plugin == other.plugin


class LyricLine:
    """Line.

    A singular lyric line within the song.
    """

    __slots__: typing.Sequence[str] = (
        "_duration",
        "_line",
        "_plugin",
        "_timestamp",
    )

    @property
    def timestamp(self) -> int:
        """The timestamp of the line in milliseconds."""
        return self._timestamp

    @property
    def duration(self) -> int:
        """The duration of the line in milliseconds."""
        return self._duration

    @property
    def line(self) -> str:
        """The lyrics line."""
        return self._line

    @property
    def plugin(self) -> typing.Mapping[str, typing.Any]:
        """Additional plugin specific data."""
        return self._plugin

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LyricLine):
            return False

        if self.timestamp != other.timestamp:
            return False

        if self.duration != other.duration:
            return False

        if self.line != other.line:
            return False

        return self.plugin == other.plugin
