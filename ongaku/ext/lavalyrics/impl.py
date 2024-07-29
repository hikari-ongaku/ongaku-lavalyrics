from __future__ import annotations

import typing

from ongaku.ext.lavalyrics import abc as abc_

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
