# ╔═════════════╗
# ║ Arc example ║
# ╚═════════════╝


import arc
import hikari

import ongaku
from ongaku.ext import injection
from ongaku.ext import checker
from ongaku.ext import lavalyrics

bot = hikari.GatewayBot("...")

client = arc.GatewayClient(bot)

ongaku_client = ongaku.Client.from_arc(client)

ongaku_client.add_extension(lavalyrics.Extension, lavalyrics.Extension(ongaku_client))

ongaku_client.create_session(
    "arc-session",
    host="127.0.0.1",
    password="youshallnotpass"
)


# ╔══════════╗
# ║ Commands ║
# ╚══════════╝


@client.include
@arc.slash_command("play", "Play a song.")
async def play_command(
    ctx: arc.GatewayContext,
    query: arc.Option[str, arc.StrParams("The song you wish to play.")],
    music: ongaku.Client = arc.inject(),
) -> None:
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

    if checker.check(query):
        result = await ongaku_client.rest.load_track(query)
    else:
        result = await ongaku_client.rest.load_track(f"ytsearch:{query}")

    if result is None:
        await ctx.respond(
            "Sorry, no songs were found.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    track: ongaku.Track

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
    except ongaku.PlayerMissingError:
        player = ongaku_client.create_player(ctx.guild_id)

    if player.connected is False:
        await player.connect(voice_state.channel_id)

    try:
        await player.play(track)
    except Exception as e:
        raise e

    await ctx.respond(
        embed=embed,
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@client.include
@arc.with_hook(injection.arc_ensure_player)
@arc.slash_command("lyrics", "View the lyrics for the current song!")
async def lyrics_command(
    ctx: arc.GatewayContext,
    player: ongaku.Player = arc.inject(),
) -> None:
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
