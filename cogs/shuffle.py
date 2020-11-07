from discord.ext import commands
from . import check_voice_connection
from utils import formatDuration


class Shuffle(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="shuffle")
    @commands.check(check_voice_connection)
    async def shuffle(self, ctx) -> None:
        VC = self.Bot.Audio.getVC(ctx.guild.id)
        Queue: dict = await VC.getQueue()

        if not Queue:
            return await ctx.send("> 🎵  셔플할 노래가 대기열에 없어요!")

        await VC.shuffle()

        return await ctx.send(f"> 🎵  재생목록에 있는 노래 {len(Queue)} 개를 셔플했어요!")


def setup(Bot):
    Bot.add_cog(Shuffle(Bot))