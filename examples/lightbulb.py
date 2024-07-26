# ╔═══════════════════╗
# ║ Lightbulb Example ║
# ╚═══════════════════╝


import hikari
import lightbulb

import ongaku
from ongaku.ext import lavalyrics

bot = lightbulb.BotApp(token="...f", banner=None)

ongaku_client = ongaku.Client(bot)

ongaku_client.add_extension(lavalyrics.Extension, lavalyrics.Extension(ongaku_client))

ongaku_client.create_session(
    "lightbulb-session",
    host="127.0.0.1",
    password="youshallnotpass"
)


# ╔══════════╗
# ║ Commands ║
# ╚══════════╝


@bot.command
@lightbulb.option("query", "Play a song. (must be a name, not a url.)")
@lightbulb.command("play", "play a song")
@lightbulb.implements(lightbulb.SlashCommand)
async def play_command(ctx: lightbulb.Context) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    voice_state = bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)
    if not voice_state or not voice_state.channel_id:
        await ctx.respond(
            "you are not in a voice channel.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    query = ctx.options.query

    if query is None or not isinstance(query, str):
        await ctx.respond("A query is required.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    await ctx.respond(
        hikari.ResponseType.DEFERRED_MESSAGE_CREATE, flags=hikari.MessageFlag.EPHEMERAL
    )

    result = await ongaku_client.rest.load_track(query)

    if result is None:
        await ctx.respond(
            hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
            "Sorry, no songs were found.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    track: ongaku.Track | None = None

    if isinstance(result, ongaku.Playlist):
        track = result.tracks[0]

    elif isinstance(result, ongaku.Track):
        track = result

    else:
        track = result[0]

    embed = hikari.Embed(
        title=f"[{track.info.title}]({track.info.uri})",
        description=f"made by: {track.info.author}",
    )

    try:
        player = ongaku_client.fetch_player(ctx.guild_id)
    except Exception:
        player = ongaku_client.create_player(ctx.guild_id)

    await player.play(track)

    await ctx.respond(
        hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
        embed=embed,
        flags=hikari.MessageFlag.EPHEMERAL,
    )



@bot.command
@lightbulb.command("lyrics", "View the lyrics for the current song!")
async def lyrics_command(
    ctx: lightbulb.Context
) -> None:
    if ctx.guild_id is None:
        await ctx.respond("You must be in a guild to run this command.")
        return

    try:
        player = ongaku_client.fetch_player(ctx.guild_id)
    except Exception:
        player = ongaku_client.create_player(ctx.guild_id)

    lyrics = player.session.client.get_extension(lavalyrics.Extension)

    if player.session.session_id is None:
        raise Exception("Session ID should not be none.")
    
    if player.track is None:
        await ctx.respond("You can't fetch the lyrics if your not playing a song!")
        return
    
    lyrics = await lyrics.fetch_lyrics_from_playing(player.session.session_id, player.guild_id)

    if lyrics is None:
        await ctx.respond("Could not find lyrics for the requested track.")
        return

    embed = hikari.Embed(
        title=f"Lyrics for {player.track.info.title}",
        description="\n".join([lyric.line for lyric in lyrics.lines])
    )

    await ctx.respond(embed=embed)


if __name__ == "__main__":
    bot.run()
