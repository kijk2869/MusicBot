from discord.ext import commands
from . import check_voice_connection
from utils import formatDuration


class Play(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="play")
    @commands.check(check_voice_connection)
    async def play(self, ctx, Query: str) -> None:
        VC = self.Bot.Audio.getVC(ctx.guild.id)
        message = await ctx.send("> ⏳  노래 로드 중...")

        Data = await VC.loadSource(Query)

        if isinstance(Data, list):
            Data = Data[0]

        Source, Index = Data["data"], Data["index"] + 1

        if Index == 1:
            await message.edit(
                content=f'> 🎵  **{Source["title"]} [{formatDuration(Source["duration"])}]**이 곧 재생되어요!'
            )
        else:
            await message.edit(
                content=f'> 🎵  **{Source["title"]} [{formatDuration(Source["duration"])}]**이 대기열 **{Index}**번에 추가되었어요!'
            )


def setup(Bot):
    Bot.add_cog(Play(Bot))