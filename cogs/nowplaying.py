import asyncio

import discord
from discord.ext import commands

from utils import formatDuration, getProgress

from . import check_voice_connection

STATE_EMOJI = {"playing": "▶️", "paused": "⏸️", "stopped": "⏹️"}


class Nowplaying(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user) -> None:
        VC = self.Bot.Audio.getVC(reaction.message.guild.id, safe=True)

        if not VC or user.bot:
            return

        if VC._np_message and VC._np_message.id == reaction.message.id:
            State: dict = await VC.getState()

            if str(reaction.emoji) == "🌟":
                Autoplay: bool = await VC.setAutoplay(
                    False if State["options"]["autoplay"] else True
                )

                await reaction.message.channel.send(
                    f"> 🌟  추천곡 기능이 **{'켜짐' if Autoplay else '꺼짐'}** 으로 설정되었어요!"
                )
            elif str(reaction.emoji) == "📌":
                VC._np_pinned = False if VC._np_pinned else True

                await VC._np_message.edit(
                    embed=reaction.message.embeds[0].set_footer(
                        text=f"노래 출처: {State['current']['uploader']} | {State['remainQueue']} 곡 남음"
                        + ("| 📌" if VC._np_pinned else "")
                    )
                )

            try:
                await reaction.message.remove_reaction(reaction, user)
            except:
                pass

    @commands.command(name="nowplaying", aliases=["np"])
    @commands.check(check_voice_connection)
    async def nowplaying(self, ctx) -> None:
        VC = self.Bot.Audio.getVC(ctx.guild.id)

        VC._np_pinned = False

        async def make_embed() -> discord.Embed:
            State: dict = await VC.getState()

            if not State.get("current"):
                embed = discord.Embed(title="아무 노래도 재생중이지 않아요!")
            else:
                embed = discord.Embed(
                    title=State["current"]["title"],
                    url=State["current"]["webpage_url"],
                    description=(
                        f"> ❤️ 음성 전송 서버: **{VC.Node.region}**\n"
                        + f"{STATE_EMOJI[State['state']]} "
                        + getProgress(State["position"], State["duration"])
                        + f" `[{formatDuration(State['position'])}/{formatDuration(State['duration'])}]`"
                        + f" 🔉 **{round(State['options']['volume'] * 100)}%**"
                    ),
                )
                embed.set_thumbnail(url=State["current"]["thumbnail"])
                embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
                embed.set_footer(
                    text=f"노래 출처: {State['current']['uploader']} | {State['remainQueue']} 곡 남음"
                    + ("| 📌" if VC._np_pinned else "")
                )

            embed.colour = ctx.guild.me.colour

            return embed

        async def task() -> None:
            VC._np_message = None

            while not ctx.bot.is_closed():
                embed: discord.Embed = await make_embed()

                if (
                    VC._np_pinned
                    and VC._np_message
                    and VC._np_message.channel.last_message_id != VC._np_message.id
                ):
                    ctx.bot.loop.create_task(VC._np_message.delete())

                    VC._np_message = None

                if not VC._np_message:
                    VC._np_message = await ctx.send(embed=embed)

                    ctx.bot.loop.create_task(
                        asyncio.wait(
                            map(
                                lambda emoji: VC._np_message.add_reaction(emoji),
                                ["🌟", "📌"],
                            )
                        )
                    )
                else:
                    try:
                        await VC._np_message.edit(embed=embed)
                    except:
                        VC._np_message = None

                await asyncio.sleep(5)

        if hasattr(VC, "_np_task") and not VC._np_task.done():
            VC._np_task.cancel()

        VC._np_task = ctx.bot.loop.create_task(task())


def setup(Bot):
    Bot.add_cog(Nowplaying(Bot))
