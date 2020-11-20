from discord.ext import commands
from . import check_voice_connection
import re
import discord
import asyncio

URL_REGEX = re.compile(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)


class SubtitleCallback:
    def __init__(self, channel: discord.TextChannel):
        self.loop = asyncio.get_event_loop()

        self._message: discord.Message = None
        self.channel: discord.TextChannel = channel

    async def callback(self, subtitle: str) -> None:
        if not self._message or self.channel.last_message.id != self._message.id:
            if self._message:
                self.loop.create_task(self._message.delete())

            self._message = await self.channel.send(
                f'{subtitle.get("previous", "")}\n> {subtitle["current"]}\n{subtitle.get("next", "")}'
            )
        else:
            await self._message.edit(
                content=f'{subtitle.get("previous", "")}\n> {subtitle["current"]}\n{subtitle.get("next", "")}'
            )


class Subtitles(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="subtitles")
    @commands.check(check_voice_connection)
    async def subtitles(self, ctx, value: str = None) -> None:
        VC = self.Bot.Audio.getVC(ctx.guild.id)
        State: dict = await VC.getState()
        usableSubtitles: list = State.get("current", {}).get("subtitles", {}).keys()

        if not value:
            return await ctx.send(
                f"> 사용 가능한 자막: {' '.join(map(lambda x: f'`{x}`', usableSubtitles))}"
            )

        urlMatch = URL_REGEX.match(value)
        if urlMatch:
            url, value = value, None
        else:
            url = None

        if value and value not in usableSubtitles:
            return await ctx.send(
                f"> ❎  `{value}` 자막을 찾을 수 없어요.\n> \n> 사용 가능한 자막: {' '.join(map(lambda x: f'`{x}`', usableSubtitles))}"
            )

        Data = await VC.getSubtitle(
            lang=value, url=url, callback=SubtitleCallback(ctx.channel).callback
        )

        await ctx.send(f"> ➡️  {f'`{value}` ' if value else ''}자막을 출력할게요!")


def setup(Bot):
    Bot.add_cog(Subtitles(Bot))