from discord.ext import commands

from utils import formatDuration

from . import check_voice_connection


class Play(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="play")
    @commands.check(check_voice_connection)
    async def play(self, ctx, *, Query: str) -> None:
        message = await ctx.send("> ⏳  노래 로드 중...")

        Data = await ctx.voice_client.loadSource(Query)

        if isinstance(Data, list):
            Data = Data[0]

        Index = ctx.voice_client.Queue.index(Data)

        if Index == 1:
            await message.edit(
                content=f"> 🎵  **{Data.title} [{formatDuration(Data.duration)}]**이 곧 재생되어요!"
            )
        else:
            await message.edit(
                content=f"> 🎵  **{Data.title} [{formatDuration(Data.duration)}]**이 대기열 **{Index}**번에 추가되었어요!"
            )


def setup(Bot):
    Bot.add_cog(Play(Bot))
