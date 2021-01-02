import discord
from discord.ext import commands

NEWLINE = "\n"


class Nodes(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="connectnodes")
    async def nodeinfo(self, ctx) -> None:
        def getText() -> str:
            return f"""
> **Discodo Node Connection**
> 
{NEWLINE.join(map(lambda x: '> '+('🛠️  `' if not x.is_connected else '✅  `') + x.region + '`', ctx.bot.Audio.Nodes))}
"""

        message = await ctx.send(getText())

        for Node in ctx.bot.Audio.Nodes:
            try:
                await Node.connect()
            finally:
                await message.edit(content=getText())


def setup(Bot):
    Bot.add_cog(Nodes(Bot))
