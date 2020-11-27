from typing import Any, Callable, Coroutine, Dict

from discord.ext import commands

from utils import formatDuration


def setup(Bot: commands.Bot) -> None:
    Audio = Bot.Audio

    def check_channel(func: Callable) -> Coroutine:
        async def wrapper(VC, *args, **kwargs) -> Any:
            if not hasattr(VC, "channel"):
                return

            return await func(VC, *args, **kwargs)

        return wrapper

    @Audio.event("SOURCE_START")
    @check_channel
    async def sendPlaying(VC, Data: Dict[str, Any]) -> None:
        await VC.channel.send(
            "> "
            + ("🌟  추천 영상" if Data["source"].get("related", False) else "🎵  현재")
            + f' 재생 중: **{Data["source"]["title"]} [{formatDuration(Data["source"]["duration"])}]**'
        )
