from __future__ import annotations

import typing

__all__ = ("Lyrics", "LyricLine")


class Lyrics:
    """Lyrics.

    A lyrics object.
    """

    __slots__: typing.Sequence[str] = (
        "_source_name",
        "_provider",
        "_text",
        "_lines",
        "_plugin",
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
        "_timestamp",
        "_duration",
        "_line",
        "_plugin",
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


# MIT License

# Copyright (c) 2024-present MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
