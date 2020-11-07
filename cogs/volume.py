from discord.ext import commands

from . import check_voice_connection


class Volume(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="volume", aliases=["vol"])
    @commands.check(check_voice_connection)
    async def volume(self, ctx, value: int = None) -> None:
        VC = self.Bot.Audio.getVC(ctx.guild.id)

        if value is None:
            State: dict = await VC.getState()
            return await ctx.send(
                f"> 🔊  현재 볼륨 {round(State['options']['volume'] * 100)}%"
            )

        if value > 200:
            return await ctx.send("❎  볼륨은 **200%** 초과일수 없어요!")
        elif value <= 0:
            return await ctx.send("❎  볼륨은 최소 **1%** 여야 해요!")

        await VC.setVolume(value / 100)

        return await ctx.send(f"> 🔊  볼륨이 **{value}%** 로 변경되었어요!")


def setup(Bot):
    Bot.add_cog(Volume(Bot))
