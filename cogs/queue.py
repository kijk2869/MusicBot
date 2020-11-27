from typing import Any, Dict, List

from discord.ext import commands

from . import check_voice_connection


class Queue(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="queue")
    @commands.check(check_voice_connection)
    async def queue(self, ctx) -> None:
        VC = self.Bot.Audio.getVC(ctx.guild.id)

        Queue: List[Dict[str, Any]] = await VC.getQueue()

        if not Queue:
            return await ctx.invoke(self.Bot.get_command("nowplaying"))


def setup(Bot):
    Bot.add_cog(Queue(Bot))
