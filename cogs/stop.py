from discord.ext import commands

from . import only_in_voice


class Stop(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="stop")
    @commands.check(only_in_voice)
    async def stop(self, ctx) -> None:
        VC = self.Bot.Audio.getVC(ctx.guild.id)

        await VC.destroy()

        await ctx.send("> 🎵  재생중인 음악을 정지하고 대기열을 초기화했어요!")


def setup(Bot):
    Bot.add_cog(Stop(Bot))
