import typing

import hikari
import lightbulb

import ongaku
from ongaku.ext.lavalyrics import LavaLyricsExtension

bot = lightbulb.BotApp(token="...f", banner=None)

ongaku_client = ongaku.Client(bot)

bot.d.music_client = ongaku_client

ongaku_client.add_extension(LavaLyricsExtension(ongaku_client))

ongaku_client.create_session(
    "lightbulb-session", host="127.0.0.1", password="youshallnotpass"
)


@bot.command
@lightbulb.option("query", "The song you wish to play.", type=str)
@lightbulb.command("lyrics", "View the lyrics of a song!")
async def lyrics_command(ctx: lightbulb.Context) -> None:
    music_client: ongaku.Client = ctx.bot.d.music_client

    query = ctx.options.query

    if query is None or not isinstance(query, str):
        await ctx.respond(
            "Invalid query, or query was not provided.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    result = await music_client.rest.load_track(query)

    if result is None:
        await ctx.respond(
            "Could not find requested track.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    ll = music_client.get_extension(LavaLyricsExtension)

    if isinstance(result, typing.Sequence):
        track = result[0]

    elif isinstance(result, ongaku.Playlist):
        await ctx.respond(
            "I cannot find lyrics for a playlist!", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    else:
        track = result

    lyrics = await ll.fetch_lyrics(track)

    if lyrics is None:
        await ctx.respond(
            "Could not find lyrics for the requested track.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    embed = hikari.Embed(
        title=f"Lyrics for {track.info.title}",
        description="\n".join([lyric.line for lyric in lyrics.lines]),
    )

    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


if __name__ == "__main__":
    bot.run()
