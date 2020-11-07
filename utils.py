from typing import Union


def getProgress(value: Union[int, float], Total: Union[int, float]) -> str:
    position_front = round(value / Total * 10)
    position_back = 10 - position_front

    return "▬" * position_front + "🔘" + "▬" * position_back


def formatDuration(seconds: int) -> str:
    seconds = int(seconds)
    minute, second = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)

    return (f"{hour:02}:" if hour else "") + f"{minute:02}:{second:02}"
