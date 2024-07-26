# ╔══════════════════╗
# ║ Crescent example ║
# ╚══════════════════╝


import dataclasses

import crescent
import hikari

import ongaku
from ongaku.ext import checker
from ongaku.ext import lavalyrics


@dataclasses.dataclass
class OngakuModel:
    ongaku_client: ongaku.Client


bot = hikari.GatewayBot("...")

ongaku_client = ongaku.Client(bot)

ongaku_client.add_extension(lavalyrics.Extension, lavalyrics.Extension(ongaku_client))

ongaku_client.create_session(
    "crescent-session",
    host="127.0.0.1",
    password="youshallnotpass"
)

client = crescent.Client(bot, OngakuModel(ongaku_client))


# ╔══════════╗
# ║ Commands ║
# ╚══════════╝


@client.include
@crescent.command(name="play", description="Play a song in a voice channel.")
class Play:
    query = crescent.option(str, "The song you wish to play.")

    async def callback(self, ctx: crescent.Context):
        if ctx.guild_id is None:
            await ctx.respond(
                "This command must be ran in a guild.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        voice_state = bot.cache.get_voice_state(ctx.guild_id, ctx.user.id)
        if not voice_state or not voice_state.channel_id:
            await ctx.respond(
                "you are not in a voice channel.", flags=hikari.MessageFlag.EPHEMERAL
            )
            return

        if checker.check(self.query):
            result = await ongaku_client.rest.load_track(self.query)
        else:
            result = await ongaku_client.rest.load_track(f"ytsearch:{self.query}")

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
            player = await ctx.client.model.ongaku_client.player.fetch(ctx.guild_id)
        except ongaku.PlayerMissingError:
            player = await ctx.client.model.ongaku_client.player.create(ctx.guild_id)

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
@crescent.command(name="lyrics", description="View the lyrics for the current song!")
class Lyrics:
    query = crescent.option(str, "The song you wish to play.")

    async def callback(self, ctx: crescent.Context):
        
        try:
            player = ctx.client.model.ongaku_client.fetch_player(ctx.guild_id)
        except ongaku.PlayerMissingError:
            player = ctx.client.model.ongaku_client.create_player(ctx.guild_id)
        
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
