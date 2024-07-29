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

for more about how to get started see the [docs](https://lavalyrics.ongaku.mplaty.com/gs/)

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

# Add a session to ongaku
client.create_session(
    "hikari-session", host="127.0.0.1", password="youshallnotpass"
)

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

    # Make sure the lyrics were not None.
    if lyrics is None:
        await bot.rest.create_message(
            event.channel_id,
            "Could not find lyrics for the requested track.",
            reply=event.message,
        )
        return

    # Turn lyrics into an embed.
    embed = hikari.Embed(
        title=f"Lyrics for {track.info.title}",
        description="\n".join([lyric.line for lyric in lyrics.lines])
    )

    # Send the lyrics as an embed.
    await bot.rest.create_message(
        event.channel_id,
        embed=embed,
        reply=event.message,
    )
```

### Issues and support

For general usage help or questions, see the `#ongaku` channel in the [hikari discord](https://discord.gg/hikari), if you have found a bug or have a feature request, feel free to [open an issue](https://github.com/hikari-ongaku/ongaku-lavalyrics/issues/new).

### Links

- [**Documentation**](https://lavalyrics.ongaku.mplaty.com)
- [**Examples**](https://github.com/hikari-ongaku/ongaku-lavalyrics/tree/main/examples)
- [**License**](https://github.com/hikari-ongaku/ongaku-lavalyrics/blob/main/LICENSE)
