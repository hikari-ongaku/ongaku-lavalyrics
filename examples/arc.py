import typing

import arc
import hikari

import ongaku
from ongaku.ext.lavalyrics import LavaLyricsExtension

bot = hikari.GatewayBot("...")

client = arc.GatewayClient(bot)

ongaku_client = ongaku.Client.from_arc(client)

ongaku_client.add_extension(LavaLyricsExtension)

ongaku_client.create_session(
    "arc-session", host="127.0.0.1", password="youshallnotpass"
)


@client.include
@arc.slash_command("lyrics", "View the lyrics of a song!")
async def lyrics_command(
    ctx: arc.GatewayContext,
    query: arc.Option[str, arc.StrParams("The song you wish to search for.")],
    music: ongaku.Client = arc.inject(),
    lavalyrics: LavaLyricsExtension = arc.inject()
) -> None:
    result = await music.rest.load_track(query)

    if result is None:
        await ctx.respond(
            "Could not find requested track.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    if isinstance(result, typing.Sequence):
        track = result[0]

    elif isinstance(result, ongaku.Playlist):
        await ctx.respond(
            "I cannot find lyrics for a playlist!", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    else:
        track = result

    lyrics = await lavalyrics.fetch_lyrics(track)

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


@client.include
@arc.slash_command("current-lyrics", "View the currently playing lyrics of a song!")
async def current_lyrics_command(
    ctx: arc.GatewayContext,
    player: ongaku.Player = arc.inject(),
    lavalyrics: LavaLyricsExtension = arc.inject()
) -> None:
    if player.track is None:
        await ctx.respond(
            "No song is currently playing!", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    session_id = player.session.session_id

    if session_id is None:
        await ctx.respond(
            "The session that the player is in has not been started.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    lyrics = await lavalyrics.fetch_lyrics_from_playing(session_id, player.guild_id)

    if lyrics is None:
        await ctx.respond(
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
        await ctx.respond("No lyrics in payload :/", flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


if __name__ == "__main__":
    bot.run()
