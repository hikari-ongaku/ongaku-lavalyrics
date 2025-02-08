import typing

import hikari
import tanjun

import ongaku
from ongaku.ext.lavalyrics import LavaLyricsExtension

bot = hikari.GatewayBot("...")

client = tanjun.Client.from_gateway_bot(bot)

ongaku_client = ongaku.Client.from_tanjun(client)

ongaku_client.add_extension(LavaLyricsExtension(ongaku_client))

ongaku_client.create_session(
    "tanjun-session", host="127.0.0.1", password="youshallnotpass"
)


component = tanjun.Component()


@component.with_slash_command
@tanjun.with_str_slash_option("query", "The song you wish to play.")
@tanjun.as_slash_command("lyrics", "View the lyrics for the current song!")
async def lyrics_command(
    ctx: tanjun.abc.SlashContext, query: str, music: ongaku.Client = tanjun.inject()
) -> None:
    result = await music.rest.load_track(query)

    if result is None:
        await ctx.create_initial_response(
            "Could not find requested track.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    ll = music.get_extension(LavaLyricsExtension)

    if isinstance(result, typing.Sequence):
        track = result[0]

    elif isinstance(result, ongaku.Playlist):
        await ctx.create_initial_response(
            "I cannot find lyrics for a playlist!", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    else:
        track = result

    lyrics = await ll.fetch_lyrics(track)

    if lyrics is None:
        await ctx.create_initial_response(
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
        await ctx.create_initial_response("No lyrics in payload :/", flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    await ctx.create_initial_response(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@component.with_slash_command
@tanjun.as_slash_command(
    "current-lyrics", "View the currently playing lyrics of a song!"
)
async def current_lyrics_command(
    ctx: tanjun.abc.SlashContext,
    player: ongaku.Player = tanjun.inject(),
) -> None:
    ll = player.session.client.get_extension(LavaLyricsExtension)

    if player.track is None:
        await ctx.create_initial_response(
            "No song is currently playing!", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    session_id = player.session.session_id

    if session_id is None:
        await ctx.create_initial_response(
            "The session that the player is in has not been started.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    lyrics = await ll.fetch_lyrics_from_playing(session_id, player.guild_id)

    if lyrics is None:
        await ctx.create_initial_response(
            "Could not find lyrics for the requested track.",
            flags=hikari.MessageFlag.EPHEMERAL,
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
        await ctx.create_initial_response("No lyrics in payload :/", flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    await ctx.create_initial_response(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


if __name__ == "__main__":
    client.add_component(component)
    bot.run()
