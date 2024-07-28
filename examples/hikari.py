import typing

import hikari

import ongaku
from ongaku.ext.lavalyrics import LavaLyricsExtension

bot = hikari.GatewayBot(token="...")

client = ongaku.Client(bot)

client.add_extension(LavaLyricsExtension(client))


@bot.listen()
async def message_event(event: hikari.GuildMessageCreateEvent) -> None:
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

    embed = hikari.Embed(
        title=f"Lyrics for {track.info.title}",
        description="\n".join([lyric.line for lyric in lyrics.lines]),
    )

    await bot.rest.create_message(
        event.channel_id,
        embed=embed,
        reply=event.message,
    )


if __name__ == "__main__":
    bot.run()
