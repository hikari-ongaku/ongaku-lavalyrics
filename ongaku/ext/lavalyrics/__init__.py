"""LavaLyrics.

The lavaLyrics extension for ongaku!

GitHub:
https://github.com/hikari-ongaku/ongaku-lavalyrics
Docs:
https://lavalyrics.ongaku.mplaty.com
"""

from __future__ import annotations

from ongaku.ext.lavalyrics.abc import LyricLine
from ongaku.ext.lavalyrics.abc import Lyrics
from ongaku.ext.lavalyrics.about import __author__
from ongaku.ext.lavalyrics.about import __author_email__
from ongaku.ext.lavalyrics.about import __license__
from ongaku.ext.lavalyrics.about import __maintainer__
from ongaku.ext.lavalyrics.about import __url__
from ongaku.ext.lavalyrics.about import __version__
from ongaku.ext.lavalyrics.extension import LavaLyricsExtension

__all__ = (  # noqa: RUF022
    # .about
    "__author__",
    "__author_email__",
    "__license__",
    "__maintainer__",
    "__url__",
    "__version__",
    # .abc
    "Lyrics",
    "LyricLine",
    # .extension
    "LavaLyricsExtension",
)

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
