import math
from typing import Any

from discord.ext import commands

from utils import formatDuration

from . import check_voice_connection


class Seek(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="seek")
    @commands.check(check_voice_connection)
    async def seek(self, ctx, *, timeString: str = None) -> None:
        VC = self.Bot.Audio.getVC(ctx.guild.id)
        State: dict = await VC.getState()

        if not State.get("current", {}).get("seekable", False):
            return await ctx.send("> ❎  이 곡은 탐색이 불가능한 곡이에요!")

        if timeString is None:
            return await ctx.send("> ❎  탐색할 위치를 입력해 주세요!")

        Position = State["position"]

        Operator: str = None
        if timeString.startswith(("+", "-")):
            Operator, timeString = timeString[0], timeString[1:]

        timeSecond: int = self.parseTime(timeString)
        if not timeSecond:
            return await ctx.send(
                "> ❎  정확하지 않은 탐색 시간이에요! [+|-|없음][시간]:[분]:[초] 로 입력해주세요!"
            )

        if Operator == "+":
            Position += timeSecond
        elif Operator == "-":
            Position -= timeSecond
        else:
            Position = timeSecond

        if Position > State["duration"]:
            return await ctx.send("> ❎  탐색 시간은 곡 길이보다 길 수 없어요!")
        if Position < 0:
            return await ctx.send("> ❎  탐색 시간은 0초보다 작을수 없어요!")

        await VC.seek(Position)

        return await ctx.send(
            f"> 🎵  **{State['current']['title']}** 곡의 **{formatDuration(Position)}** 으로 점프했어요!"
        )

    def parseTime(self, input: Any) -> int:
        if str(input).isdigit():
            return int(input)

        input: str = str(input)

        def tokenize(value: str) -> float:
            try:
                value: float = value

                if math.isinf(value) or math.isnan(value):
                    return

                return value
            except ValueError:
                return

        try:
            Tokenized: list = list(filter(map(tokenize, input.split(":"))))
        except:
            return

        if not Tokenized:
            return

        Tokenized.reverse()

        try:
            return sum(
                [int(Token) * (60 ** index) for index, Token in enumerate(Tokenized)]
            )
        except:
            return


def setup(Bot):
    Bot.add_cog(Seek(Bot))
