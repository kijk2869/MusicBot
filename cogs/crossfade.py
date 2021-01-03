from discord.ext import commands

from . import check_voice_connection


class Crossfade(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="crossfade", aliases=["cf"])
    @commands.check(check_voice_connection)
    async def crossfade(self, ctx, value: str = None) -> None:
        VC = self.Bot.Audio.getVC(ctx.guild.id)
        State: dict = await VC.getState()

        if value is None:
            return await ctx.send(
                f"> 🔊  현재 크로스페이드 {State['options']['crossfade']:.1f}초"
            )

        Operator: str = None
        if value.startswith(("+", "-")):
            Operator, crossfadeString = value[0], value[1:]
        else:
            crossfadeString = value

        if not crossfadeString.isdigit():
            return await ctx.send("❎  크로스페이드는 [+|-|없음][초] 의 형식만 사용 가능해요!")

        Crossfade = State["options"]["crossfade"]
        if Operator == "+":
            Crossfade += float(crossfadeString)
        elif Operator == "-":
            Crossfade -= float(crossfadeString)
        else:
            Crossfade = float(crossfadeString)

        if Crossfade > 30:
            return await ctx.send("❎  크로스페이드는 **30초** 초과일수 없어요!")
        elif Crossfade < 0:
            return await ctx.send("❎  크로스페이드는 최소 **0초** 여야 해요!")

        await VC.setCrossfade(Crossfade)

        return await ctx.send(f"> 🔊  크로스페이드가 **{Crossfade:.1f}** 로 변경되었어요!")


def setup(Bot):
    Bot.add_cog(Crossfade(Bot))
