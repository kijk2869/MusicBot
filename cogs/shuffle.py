from discord.ext import commands

from utils import formatDuration

from . import check_voice_connection


class Shuffle(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="shuffle")
    @commands.check(check_voice_connection)
    async def shuffle(self, ctx) -> None:
        if not ctx.voice_client.Queue:
            return await ctx.send("> 🎵  셔플할 노래가 대기열에 없어요!")

        await ctx.voice_client.shuffle()

        return await ctx.send(
            f"> 🎵  재생목록에 있는 노래 {len(ctx.voice_client.Queue)} 개를 셔플했어요!"
        )


def setup(Bot):
    Bot.add_cog(Shuffle(Bot))
