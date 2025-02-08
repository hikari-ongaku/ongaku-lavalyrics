# Ongaku
A simple voice library for Hikari.

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/ongaku-lavalyrics)](https://pypi.org/project/ongaku-lavalyrics)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
![Pyright](https://badgen.net/badge/Pyright/strict/2A6DB2)
[![Ongaku](https://badgen.net/badge/Ongaku/Extension/FF6B61)](https://ongaku.mplaty.com/)

</div>

Ongaku LavaLyrics is an extension for [Ongaku](https://ongaku.mplaty.com/) that allows you to fetch lyrics for songs!

## Current Features

- Fetching Currently Playing songs
- Fetching Songs

## Installation

To install ongaku-lavalyrics, run the following command:

```sh
pip install -U ongaku-lavalyrics
```

To check if ongaku-lavalyrics has successfully installed or not, run the following command:

```sh
python3 -m ongaku-lavalyrics
# On Windows you may need to run:
py -m ongaku-lavalyrics
```

## Getting Started

```py
import typing
import hikari
import ongaku
from ongaku.ext.lavalyrics import LavaLyricsExtension

# Create a GatewayBot (RESTBot's are not supported.)
bot = hikari.GatewayBot(token="...")

# Create the ongaku client
client = ongaku.Client(bot)

# Add the LavaLyrics extension
client.add_extension(LavaLyricsExtension, LavaLyricsExtension(client))

@bot.listen()
async def message_event(
    event: hikari.GuildMessageCreateEvent
) -> None:
    # Ignore anything that has no content, is not a human, or is not in a guild.
    if not event.content or not event.is_human or not event.guild_id:
        return

    # Ignore anything that is not the lyrics command.
    if not event.content.startswith("!lyrics"):
        return

    # Get the query from lyrics "command".
    query = event.content.strip("!lyrics ")

    # Search youtube for the song.
    result = await client.rest.load_track(query)

    # Make sure the result is not None.
    if result is None:
        await bot.rest.create_message(
            event.channel_id,
            "Could not find requested track.",
            reply=event.message,
        )
        return

    # Get the extension.
    ll = client.get_extension(LavaLyricsExtension)

    # Compare the track types.
    if isinstance(result, typing.Sequence):
        track = result[0]
    
    elif isinstance(result, ongaku.Playlist):
        await bot.rest.create_message(
            event.channel_id,
            "I cannot find lyrics for a playlist!",
            reply=event.message,
        )
        return
    
    else:
        track = result
    
    # Fetch the lyrics for the song.
    lyrics = await ll.fetch_lyrics(track)

    if lyrics is None:
        await ctx.respond(
            "Could not find lyrics for the requested track.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    if len(lyrics.lines) > 0:
        embed = hikari.Embed(
            title=f"Lyrics for {track.info.title}",
            description="\n".join([lyric.line for lyric in lyrics.lines]),
        )
    elif lyrics.text:
        embed = hikari.Embed(
            title=f"Lyrics for {track.info.title}",
            description=lyrics.text,
        )
    else:
        await ctx.respond("No lyrics in payload :/", flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
```

## API Reference

### `LavaLyricsExtension`

The base Lava Lyrics Extension.

#### `fetch_lyrics_from_playing`

Fetch the lyrics from a player that is currently playing a track.

Parameters
|Name               |Type                                          |Default  |Description                                    |
|:------------------|:--------------------------------------------:|:-------:|:----------------------------------------------|
|session_id         |`str`                                         |         |The session id attached to the player.         |
|guild              |`hikari.SnowflakeishOr[hikari.PartialGuild]`  |         |The guild or guild id the player is in.        |
|skip_track_source  |`bool`                                        |`False`  |Whether to skip the tracks source for lyrics.  |
|session            |`Session`, `None`                             |`None`   |The session to use to fetch information from.  |

Raises
|Type                                                                                        |Description                                                                          |
|:-------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------|
|[`NoSessionsError`](https://ongaku.mplaty.com/api/errors/#ongaku.errors.NoSessionsError)    |Raised when there is no available sessions for this request to take place.           |
|[`TimeoutError`](https://ongaku.mplaty.com/api/errors/#ongaku.errors.TimeoutError)          |Raised when the request takes too long to respond.                                   |
|[`RestStatusError`](https://ongaku.mplaty.com/api/errors/#ongaku.errors.RestStatusError)    |Raised when a 4XX or a 5XX status is received.                                       |
|[`BuildError`](https://ongaku.mplaty.com/api/errors/#ongaku.errors.BuildError)              |Raised when the lyrics could not be built.                                           |
|[`RestRequestError`](https://ongaku.mplaty.com/api/errors/#ongaku.errors.RestRequestError)  |Raised when a 4XX or a 5XX status is received, and lavalink gives more information.  |
|[`RestError`](https://ongaku.mplaty.com/api/errors/#ongaku.errors.RestError)                |Raised when an unknown error is caught.                                              |

Returns
|Type                 |Description                                                                          |
|:--------------------|:------------------------------------------------------------------------------------|
|[`Lyrics`](#lyrics)  |If successfully found, a [Lyrics](#lyrics) object.                                   |
|`None`               |If the lyrics do not exist for the track, or if the track requested does not exist.  |

#### `fetch_lyrics`

Fetch the lyrics of a specified track, or its encoded value.

Parameters
|Name               |Type                      |Default  |Description                                           |
|:------------------|:------------------------:|:-------:|:-----------------------------------------------------|
|track              |`ongaku.Track`, `str`     |         |The track you wish to fetch the lyrics for.           |
|skip_track_source  |`bool`                    |`False`  |Whether to skip the tracks source for lyrics or not.  |
|session            |`ongaku.Session`, `None`  |`None`   |The session to use to fetch information from.         |

Raises
|Type                                                                                        |Description                                                                          |
|:-------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------|
|[`NoSessionsError`](https://ongaku.mplaty.com/api/errors/#ongaku.errors.NoSessionsError)    |Raised when there is no available sessions for this request to take place.           |
|[`TimeoutError`](https://ongaku.mplaty.com/api/errors/#ongaku.errors.TimeoutError)          |Raised when the request takes too long to respond.                                   |
|[`RestStatusError`](https://ongaku.mplaty.com/api/errors/#ongaku.errors.RestStatusError)    |Raised when a 4XX or a 5XX status is received.                                       |
|[`BuildError`](https://ongaku.mplaty.com/api/errors/#ongaku.errors.BuildError)              |Raised when the lyrics could not be built.                                           |
|[`RestRequestError`](https://ongaku.mplaty.com/api/errors/#ongaku.errors.RestRequestError)  |Raised when a 4XX or a 5XX status is received, and lavalink gives more information.  |
|[`RestError`](https://ongaku.mplaty.com/api/errors/#ongaku.errors.RestError)                |Raised when an unknown error is caught.                                              |

Returns
|Type                 |Description                                                                          |
|:--------------------|:------------------------------------------------------------------------------------|
|[`Lyrics`](#lyrics)  |If successfully found, a [Lyrics](#lyrics) object.                                   |
|`None`               |If the lyrics do not exist for the track, or if the track requested does not exist.  |

### Lyrics

Properties
|Name         |Value                              |Description                                                          |
|:------------|:---------------------------------:|:--------------------------------------------------------------------|
|source_name  |`str`                              |The name of the source where the lyrics were fetched from.           |
|provider     |`str`                              |The name of the provider the lyrics was fetched from on the source.  |
|text         |`str`, `None`                      |The lyrics text.                                                     |
|lines        |`typing.Sequence[LyricLine)]`      |The lyrics lines.                                                    |
|plugin       |`typing.Mapping[str, typing.Any]`  |Additional plugin specific data.                                     |

### LyricLine

Properties
|Name       |Value                              |Description                                 |
|:----------|:---------------------------------:|:-------------------------------------------|
|timestamp  |`int`                              |The timestamp of the line in milliseconds.  |
|duration   |`int`                              |The duration of the line in milliseconds.   |
|line       |`str`                              |The lyrics line.                            |
|plugin     |`typing.Mapping[str, typing.Any]`  |Additional plugin specific data.            |

## Issues and support

For general usage help or questions, see the `#ongaku` channel in the [hikari discord](https://discord.gg/hikari), if you have found a bug or have a feature request, feel free to [open an issue](https://github.com/hikari-ongaku/ongaku-lavalyrics/issues/new).

### Links

- [**Examples**](https://github.com/hikari-ongaku/ongaku-lavalyrics/tree/main/examples)
- [**License**](https://github.com/hikari-ongaku/ongaku-lavalyrics/blob/main/LICENSE)
