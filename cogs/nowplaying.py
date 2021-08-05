import asyncio

import discord
from discord.ext import commands
from discodo.enums import PlayerState


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
            if str(reaction.emoji) == "🌟":
                await VC.setAutoplay(not VC.autoplay)

                await reaction.message.channel.send(
                    f"> 🌟  추천곡 기능이 **{'켜짐' if VC.autoplay else '꺼짐'}** 으로 설정되었어요!"
                )
            elif str(reaction.emoji) == "📌":
                VC._np_pinned = False if VC._np_pinned else True

                if VC.current:
                    await VC._np_message.edit(
                        embed=reaction.message.embeds[0].set_footer(
                            text=f"노래 출처: {VC.current.uploader} | {len(VC.Queue)} 곡 남음"
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
        ctx.voice_client._np_pinned = False

        async def make_embed() -> discord.Embed:
            if not ctx.voice_client.current:
                embed = discord.Embed(title="I'm not playing anything!")
            else:
                Chapters = list(
                    filter(
                        lambda x: x["start_time"]
                        <= ctx.voice_client.current.position
                        < x["end_time"],
                        ctx.voice_client.current.get("chapters") or [],
                    )
                )
                Chapter = Chapters[0] if Chapters else None

                STATE_EMOJI = {
                    PlayerState.PLAYING: "▶️",
                    PlayerState.PAUSED: "⏸️",
                    PlayerState.STOPPED: "⏹️",
                }

                embed = discord.Embed(
                    title=ctx.voice_client.current.title,
                    url=ctx.voice_client.current.webpage_url,
                    description=(
                        (
                            f"- `[{formatDuration(Chapter['start_time'])} ~ {formatDuration(Chapter['end_time'])}]` **{Chapter['title']}**\n\n"
                            if Chapter
                            else ""
                        )
                        + f"{STATE_EMOJI[ctx.voice_client.state]} "
                        + getProgress(
                            ctx.voice_client.current.position, ctx.voice_client.duration
                        )
                        + f" `[{formatDuration(ctx.voice_client.current.position)}/{formatDuration(ctx.voice_client.current.duration)}]`"
                        + f" 🔉 **{round(ctx.voice_client.volume * 100)}%**"
                    ),
                )
                if ctx.voice_client.current.thumbnail:
                    embed.set_thumbnail(url=ctx.voice_client.current.thumbnail)

                embed.set_footer(
                    text=f"노래 출처: {ctx.voice_client.current.uploader} | {len(ctx.voice_client.Queue)} 곡 남음"
                    + ("| 📌" if ctx.voice_client._np_pinned else "")
                )

            embed.colour = ctx.guild.me.colour

            return embed

        async def task() -> None:
            ctx.voice_client._np_message = None

            while not ctx.bot.is_closed():
                embed: discord.Embed = await make_embed()

                if (
                    ctx.voice_client._np_pinned
                    and ctx.voice_client._np_message
                    and ctx.voice_client._np_message.channel.last_message_id
                    != ctx.voice_client._np_message.id
                ):
                    ctx.bot.loop.create_task(ctx.voice_client._np_message.delete())

                    ctx.voice_client._np_message = None

                if not ctx.voice_client._np_message:
                    ctx.voice_client._np_message = await ctx.send(embed=embed)
                else:
                    try:
                        await ctx.voice_client._np_message.edit(embed=embed)
                    except:
                        ctx.voice_client._np_message = None

                await asyncio.sleep(5)

        if (
            hasattr(ctx.voice_client, "_np_task")
            and not ctx.voice_client._np_task.done()
        ):
            ctx.voice_client._np_task.cancel()

        ctx.voice_client._np_task = ctx.bot.loop.create_task(task())


def setup(Bot):
    Bot.add_cog(Nowplaying(Bot))
