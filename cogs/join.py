from discord.ext import commands

from . import check_voice_connection


class Join(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="join")
    @commands.check(check_voice_connection)
    async def join(self, ctx) -> None:
        return


def setup(Bot):
    Bot.add_cog(Join(Bot))
