from discord.ext import commands

from . import check_voice_connection


class Volume(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="volume", aliases=["vol"])
    @commands.check(check_voice_connection)
    async def volume(self, ctx, value: str = None) -> None:
        VC = self.Bot.Audio.getVC(ctx.guild.id)
        State: dict = await VC.getState()

        if value is None:
            return await ctx.send(
                f"> 🔊  현재 볼륨 {round(State['options']['volume'] * 100)}%"
            )

        Operator: str = None
        if value.startswith(("+", "-")):
            Operator, volumeString = value[0], value[1:]
        else:
            volumeString = value

        if not volumeString.isdigit():
            return await ctx.send("❎  볼륨은 [+|-|없음][볼륨(정수)] 의 형식만 사용 가능해요!")

        Volume = State["options"]["volume"] * 100
        if Operator == "+":
            Volume += int(volumeString)
        elif Operator == "-":
            Volume -= int(volumeString)
        else:
            Volume = int(volumeString)

        if Volume > 200:
            return await ctx.send("❎  볼륨은 **200%** 초과일수 없어요!")
        elif Volume <= 0:
            return await ctx.send("❎  볼륨은 최소 **1%** 여야 해요!")

        await VC.setVolume(Volume / 100)

        return await ctx.send(f"> 🔊  볼륨이 **{round(Volume)}%** 로 변경되었어요!")


def setup(Bot):
    Bot.add_cog(Volume(Bot))
