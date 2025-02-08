import typing

import hikari

import ongaku
from ongaku.ext.lavalyrics import LavaLyricsExtension

bot = hikari.GatewayBot(token="...")

client = ongaku.Client(bot)

client.add_extension(LavaLyricsExtension)


@bot.listen()
async def lyrics_command_event(event: hikari.GuildMessageCreateEvent) -> None:
    if not event.content or not event.is_human or not event.guild_id:
        return

    if not event.content.startswith("!lyrics"):
        return

    query = event.content.strip("!lyrics ")

    result = await client.rest.load_track(query)

    if result is None:
        await bot.rest.create_message(
            event.channel_id,
            "Could not find requested track.",
            reply=event.message,
        )
        return

    ll = client.get_extension(LavaLyricsExtension)

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

    lyrics = await ll.fetch_lyrics(track)

    if lyrics is None:
        await bot.rest.create_message(
            event.channel_id,
            "Could not find lyrics for the requested track.",
            reply=event.message,
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
        await bot.rest.create_message(
            event.channel_id, "No lyrics in payload :/", reply=event.message
        )
        return

    await bot.rest.create_message(event.channel_id, embed=embed, reply=event.message)


@bot.listen()
async def current_lyrics_command_event(event: hikari.GuildMessageCreateEvent) -> None:
    if not event.content or not event.is_human or not event.guild_id:
        return

    if not event.content.startswith("!current-lyrics"):
        return

    player = client.fetch_player(event.guild_id)

    ll = player.session.client.get_extension(LavaLyricsExtension)

    if player.track is None:
        await bot.rest.create_message(
            event.channel_id,
            "No song is currently playing!",
            reply=event.message,
        )
        return

    session_id = player.session.session_id

    if session_id is None:
        await bot.rest.create_message(
            event.channel_id,
            "The session that the player is in has not been started.",
            reply=event.message,
        )
        return

    lyrics = await ll.fetch_lyrics_from_playing(session_id, player.guild_id)

    if lyrics is None:
        await bot.rest.create_message(
            event.channel_id,
            "Could not find lyrics for the requested track.",
            reply=event.message,
        )
        return

    if len(lyrics.lines) > 0:
        embed = hikari.Embed(
            title=f"Lyrics for {player.track.info.title}",
            description="\n".join([lyric.line for lyric in lyrics.lines]),
        )
    elif lyrics.text:
        embed = hikari.Embed(
            title=f"Lyrics for {player.track.info.title}",
            description=lyrics.text,
        )
    else:
        await bot.rest.create_message(
            event.channel_id, "No lyrics in payload :/", reply=event.message
        )
        return

    await bot.rest.create_message(event.channel_id, embed=embed, reply=event.message)


if __name__ == "__main__":
    bot.run()
