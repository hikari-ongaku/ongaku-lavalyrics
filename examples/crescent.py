import dataclasses
import typing

import crescent
import hikari

import ongaku
from ongaku.ext.lavalyrics import LavaLyricsExtension


@dataclasses.dataclass
class OngakuModel:
    ongaku_client: ongaku.Client


bot = hikari.GatewayBot("...")

ongaku_client = ongaku.Client(bot)

ongaku_client.add_extension(LavaLyricsExtension)

ongaku_client.create_session(
    "crescent-session", host="127.0.0.1", password="youshallnotpass"
)

client = crescent.Client(bot, OngakuModel(ongaku_client))


@client.include
@crescent.command(name="lyrics", description="View the lyrics for the current song!")
class Lyrics:
    query = crescent.option(str, "The song you wish to play.")

    async def callback(self, ctx: crescent.Context):
        music_client: ongaku.Client = ctx.client.model.ongaku

        result = await music_client.rest.load_track(self.query)

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
                "I cannot find lyrics for a playlist!",
                flags=hikari.MessageFlag.EPHEMERAL,
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


@client.include
@crescent.command(
    name="current-lyrics", description="View the currently playing lyrics of a song!"
)
class CurrentLyrics:
    async def callback(self, ctx: crescent.Context):
        music_client: ongaku.Client = ctx.client.model.ongaku

        if ctx.guild_id is None:
            await ctx.respond(
                "This command must be ran in a guild.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        player = music_client.fetch_player(ctx.guild_id)

        ll = player.session.client.get_extension(LavaLyricsExtension)

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

        lyrics = await ll.fetch_lyrics_from_playing(session_id, player.guild_id)

        if lyrics is None:
            await ctx.respond(
                "Could not find lyrics for the requested track.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        embed = hikari.Embed(
            title=f"Lyrics for {player.track.info.title}",
            description="\n".join([lyric.line for lyric in lyrics.lines]),
        )

        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


if __name__ == "__main__":
    bot.run()
