import math
from typing import Any, Dict

from discord.ext import commands

from utils import formatDuration

from . import check_voice_connection


class Seek(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="seek")
    @commands.check(check_voice_connection)
    async def seek(self, ctx, *, inputValue: str = None) -> None:
        timeString = inputValue

        if not ctx.voice_client.current.seekable:
            return await ctx.send("> ❎  이 곡은 탐색이 불가능한 곡이에요!")

        if timeString is not None:
            Position = ctx.voice_client.position

            Operator: str = None
            if timeString.startswith(("+", "-")):
                Operator, timeString = timeString[0], timeString[1:]

            timeSecond: int = self.parseTime(timeString)

            if timeSecond:
                if Operator == "+":
                    Position += timeSecond
                elif Operator == "-":
                    Position -= timeSecond
                else:
                    Position = timeSecond
            else:
                Position = None
        else:
            Position = None

        if Position is None:
            Chapters: Dict[str, Any] = {
                Chapter["title"].lower(): Chapter
                for Chapter in ctx.voice_client.current.chapters
            }

            SelectedChapter: Dict[str, Any] = (
                Chapters.get(inputValue.lower()) if inputValue else None
            )

            if not SelectedChapter:

                def getText(Chapter) -> str:
                    Text: str = (
                        f"`{formatDuration(Chapter['start_time'])}` {Chapter['title']}"
                    )

                    if (
                        Chapter["start_time"]
                        <= ctx.voice_client.position
                        < Chapter["end_time"]
                    ):
                        Text = "**" + Text + "**"

                    return "> " + Text

                return await ctx.send(
                    "> ❎  정확하지 않은 탐색 시간이에요! [+|-|없음][시간]:[분]:[초] 혹은 챕터 이름으로 입력해주세요!"
                    + (
                        ("\n> \n" + "\n".join(map(getText, Chapters.values())))
                        if Chapters
                        else ""
                    )
                )

            Position = SelectedChapter["start_time"]

        if Position > ctx.voice_client.duration:
            return await ctx.send("> ❎  탐색 시간은 곡 길이보다 길 수 없어요!")
        if Position < 0:
            return await ctx.send("> ❎  탐색 시간은 0초보다 작을수 없어요!")

        await ctx.voice_client.seek(Position)

        return await ctx.send(
            f"> 🎵  **{ctx.voice_client.current.title}** 곡의 **{formatDuration(Position)}** 으로 점프했어요!"
        )

    def parseTime(self, input: Any) -> int:
        if str(input).isdigit():
            return int(input)

        input: str = str(input)

        def tokenize(value: str) -> float:
            try:
                value: float = float(value)

                if math.isinf(value) or math.isnan(value):
                    return

                return value
            except ValueError:
                return

        try:
            Tokenized: list = list(
                filter(lambda x: x or x == 0, map(tokenize, input.split(":")))
            )
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
