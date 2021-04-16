from discord.ext import commands

from utils import formatDuration

from . import check_voice_connection


class Skip(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="skip")
    @commands.check(check_voice_connection)
    async def skip(self, ctx) -> None:
        if not ctx.voice_client.current:
            return await ctx.send("> 🎵  현재 노래를 재생중이지 않아요!")

        await ctx.voice_client.skip()

        return await ctx.send(
            f'> 🎵  **{ctx.voice_client.current["title"]} [{formatDuration(ctx.voice_client.duration)}]** 곡이 건너뛰어졌어요!'
        )


def setup(Bot):
    Bot.add_cog(Skip(Bot))
