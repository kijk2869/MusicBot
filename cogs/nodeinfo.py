import discord
from discord.ext import commands


class Nodeinfo(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="nodeinfo")
    async def nodeinfo(self, ctx) -> None:
        embed = discord.Embed(title="Discodo Nodes Info", colour=0x7289DA)

        for Node in ctx.bot.Audio.Nodes:
            Status: dict = await Node.getStatus()

            embed.add_field(
                name=f"{Node.region}",
                value=f"""
                **{Status['UsedMemory']} MB** Used
                **{Status['Cores']}** Cores
                **{Status['TotalLoad']}%** System Loads
                **{Status["ProcessLoad"]}%** Discodo Loads
            """,
                inline=False,
            )

        embed.set_footer(text="Powered by pypi.org/project/discodo")

        return await ctx.send(embed=embed)


def setup(Bot):
    Bot.add_cog(Nodeinfo(Bot))