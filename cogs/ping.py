from datetime import datetime
import discord
from discord.ext.commands import command, Cog
from discord.ext.commands.bot import Bot

from discord.ext.commands.context import Context
from discord.message import Message


class Ping(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @command(name="핑")
    async def _ping(self, ctx: Context):
        msg: Message = await ctx.send(
            embed=discord.Embed(title="🏓핑", description="측정중", colour=0x7289DA)
        )
        await msg.edit(
            embed=discord.Embed(
                title="🏓퐁!",
                description=f"웹소켓 핑: {round(self.bot.latency * 1000)}ms\n메세지 반응 핑: {round(msg.created_at - ctx.message.created_at).total_seconds()}ms",
                timestamp=datetime.utcnow(),
                colour=0x7289DA,
            )
        )


def setup(bot: Bot):
    bot.add_cog(Ping(bot))