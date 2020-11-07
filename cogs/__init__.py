import logging
import os
import re
import traceback
from typing import Any, Coroutine

log = logging.getLogger("musicbot.cogs")

Directory = os.path.dirname(os.path.realpath(__file__))


def load(Bot):
    Failed = []

    for Extension in [
        "cogs." + re.sub(".py", "", File)
        for File in os.listdir(Directory)
        if not "__" in File
    ]:
        try:
            Bot.load_extension(Extension)
        except:
            log.error(f"while loading extension {Extension}, an error occured.")
            traceback.print_exc()
            Failed.append(Extension)

    return Failed


async def check_voice_connection(ctx) -> Any:
    if not ctx.bot.Audio.getVC(ctx.guild.id, safe=True):
        if not ctx.author.voice:
            await ctx.send("> 🎵  먼저 음성 채널에 접속해주세요!")
            return False

        message = await ctx.send(
            f"> 💡  음성 채널 {ctx.author.voice.channel.mention} 에 접속 중..."
        )
        await ctx.bot.Audio.connect(ctx.author.voice.channel)
        await message.edit(
            content=f"> 🎵  성공적으로 음성 채널 {ctx.author.voice.channel.mention} 에 접속했어요!"
        )

    return True