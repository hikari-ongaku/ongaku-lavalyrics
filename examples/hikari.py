# ╔════════════════╗
# ║ Hikari example ║
# ╚════════════════╝


import hikari

import ongaku
from ongaku.ext import checker
from ongaku.ext import lavalyrics


bot = hikari.GatewayBot("...", suppress_optimization_warning=True, intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT)

ongaku_client = ongaku.Client(bot)

ongaku_client.add_extension(lavalyrics.Extension, lavalyrics.Extension(ongaku_client))

ongaku_client.create_session(
    "hikari-session",
    host="127.0.0.1",
    password="youshallnotpass"
)


# ╔══════════╗
# ║ Commands ║
# ╚══════════╝


prefix = "!"


def handle_command(content: str, name: str) -> list[str] | None:
    if content.startswith(prefix + name):
        content = content.strip(prefix + name + " ")
        return content.split(" ")


@bot.listen()
async def play_command(
    event: hikari.GuildMessageCreateEvent
) -> None:
    if event.content is None:
        return
    
    if event.is_bot:
        return

    args = handle_command(event.content, "play")

    if args is None:
        return

    voice_state = bot.cache.get_voice_state(event.guild_id, event.author.id)
    if not voice_state or not voice_state.channel_id:
        await bot.rest.create_message(
            event.channel_id,
            "you are not in a voice channel.",
            reply=event.message,
        )
        return
    
    if checker.check(args[0]):
        result = await ongaku_client.rest.load_track(args[0])
    else:
        result = await ongaku_client.rest.load_track(f"ytsearch:{args[0]}")

    if result is None:
        await bot.rest.create_message(
            event.channel_id,
            "Sorry, no songs were found.",
            reply=event.message,
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
        player = ongaku_client.fetch_player(event.guild_id)
    except ongaku.PlayerMissingError:
        player = ongaku_client.create_player(event.guild_id)

    if player.connected is False:
        await player.connect(voice_state.channel_id)

    try:
        await player.play(track)
    except Exception as e:
        raise e

    await bot.rest.create_message(
        event.channel_id,
        embed=embed,
        reply=event.message,
    )


@bot.listen()
async def lyrics_command(
    event: hikari.GuildMessageCreateEvent
) -> None:
    if event.content is None:
        return
    
    if event.is_bot:
        return
    
    try:
        player = ongaku_client.fetch_player(event.guild_id)
    except ongaku.PlayerMissingError:
        player = ongaku_client.create_player(event.guild_id)
    
    lyrics = player.session.client.get_extension(lavalyrics.Extension)

    if player.session.session_id is None:
        raise Exception("Session ID should not be none.")
    
    if player.track is None:
        await bot.rest.create_message(
            event.channel_id,
            "You can't fetch the lyrics if your not playing a song!",
            reply=event.message,
        )
        return
    
    lyrics = await lyrics.fetch_lyrics_from_playing(player.session.session_id, player.guild_id)

    if lyrics is None:
        await bot.rest.create_message(
            event.channel_id,
            "Could not find lyrics for the requested track.",
            reply=event.message,
        )
        return

    embed = hikari.Embed(
        title=f"Lyrics for {player.track.info.title}",
        description="\n".join([lyric.line for lyric in lyrics.lines])
    )

    await bot.rest.create_message(
            event.channel_id,
            embed=embed,
            reply=event.message,
        )

if __name__ == "__main__":
    bot.run()
