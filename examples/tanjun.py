# ╔════════════════╗
# ║ Tanjun example ║
# ╚════════════════╝


import hikari
import tanjun

import ongaku
from ongaku.ext import checker
from ongaku.ext import lavalyrics

bot = hikari.GatewayBot("...")

client = tanjun.Client.from_gateway_bot(bot)

ongaku_client = ongaku.Client.from_tanjun(client)

ongaku_client.add_extension(lavalyrics.Extension, lavalyrics.Extension(ongaku_client))

ongaku_client.create_session(
    "tanjun-session",
    host="127.0.0.1",
    password="youshallnotpass"
)


# ╔══════════╗
# ║ Commands ║
# ╚══════════╝


component = tanjun.Component()


@component.with_slash_command
@tanjun.with_str_slash_option("query", "The song you wish to play.")
@tanjun.as_slash_command("play", "Play a song.")
async def play_command(
    ctx: tanjun.abc.SlashContext,
    query: str,
    ongaku_client: ongaku.Client = tanjun.inject(),
) -> None:
    if ctx.guild_id is None:
        await ctx.create_initial_response(
            "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    voice_state = bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)
    if not voice_state or not voice_state.channel_id:
        await ctx.create_initial_response(
            "you are not in a voice channel.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    if checker.check(query):
        result = await ongaku_client.rest.load_track(query)
    else:
        result = await ongaku_client.rest.load_track(f"ytsearch:{query}")

    if result is None:
        await ctx.create_initial_response(
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

    await ctx.create_initial_response(
        embed=embed,
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@component.with_slash_command
@tanjun.as_slash_command("lyrics", "View the lyrics for the current song!")
async def lyrics_command(
    ctx: tanjun.abc.SlashContext, ongaku_client: ongaku.Client = tanjun.inject()
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
    client.add_component(component)
    bot.run()
