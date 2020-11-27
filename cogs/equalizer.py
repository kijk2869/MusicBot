from typing import Any, Dict
from discord.ext import commands
import discord

from . import check_voice_connection

from PIL import Image
import io


class Equalizer(commands.Cog):
    BOARD_FREQUENCY_POS_WIDTH = {
        63: 161,
        125: 250,
        250: 346,
        500: 443,
        1000: 537,
        2000: 628,
        4000: 716,
        8000: 812,
        16000: 906,
    }

    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="equalizer", aliases=["eq"])
    @commands.check(check_voice_connection)
    async def equalizer(
        self, ctx, selectedFrequency: str = None, selectedGain: float = None
    ) -> None:
        VC = self.Bot.Audio.getVC(ctx.guild.id)
        State: dict = await VC.getState()

        Equalizer_Set = {
            63: 0.0,
            125: 0.0,
            250: 0.0,
            500: 0.0,
            1000: 0.0,
            2000: 0.0,
            4000: 0.0,
            8000: 0.0,
            16000: 0.0,
        }
        if "anequalizer" in State["options"]["filter"]:

            def applyEqualizer(LibavOption) -> None:
                def makeDict(Data):
                    if "=" not in Data:
                        return None

                    Values = Data.split("=")
                    return Values[0], Values[1]

                Options = dict(filter(None, map(makeDict, LibavOption.split(" "))))

                if not "f" in Options or not "g" in Options:
                    return

                Equalizer_Set[int(Options["f"])] = float(Options["g"])

            list(
                map(
                    applyEqualizer, State["options"]["filter"]["anequalizer"].split("|")
                )
            )

        if selectedFrequency is not None and selectedGain is not None:
            if selectedFrequency.endswith("k") and selectedFrequency[:-1].isdigit():
                selectedFrequency = str(int(selectedFrequency[:-1]) * 1000)

            if (
                not selectedFrequency.isdigit()
                or int(selectedFrequency) not in Equalizer_Set.keys()
            ):
                return await ctx.send(
                    f"> ❎  **{selectedFrequency}hz**는 설정할 수 없는 주파수에요!"
                )

            if selectedGain > 10:
                return await ctx.send("❎  매개 변수는 **10dB** 보다 클 수 없어요!")
            elif selectedGain < -10:
                return await ctx.send("❎ 매개 변수는 **-10dB** 보다 작을수 없어요!")

            Equalizer_Set[int(selectedFrequency)] = selectedGain

            State["options"]["filter"]["anequalizer"] = "|".join(
                [
                    f"c0 f={Frequency} w=100 g={Gain}|c1 f={Frequency} w=100 g={Gain}"
                    for Frequency, Gain in Equalizer_Set.items()
                    if Gain != 0
                ]
            )

            await VC.setFilter(State["options"]["filter"])

            await ctx.send(
                f"""
                > 📊  **이퀄라이저 효과**
                > 🔊 `{selectedFrequency}hz` **{selectedGain:+0.1f}dB**
                > 💡  `노래 효과는 적용되는 데에 5초에서 10초 정도 시간이 걸릴 수 있어요!`
                """
            )

        fp = await self.Bot.loop.run_in_executor(None, self.make_image, Equalizer_Set)

        await ctx.send(file=discord.File(fp, "equalizer.png"))

    def make_image(self, Equalizer_Set: Dict[str, Any]) -> io.BytesIO:
        Board = Image.open("./image/equalizer_base.png")
        Radio_Button = Image.open("./image/radio_button.png")

        for Frequency, Gain in Equalizer_Set.items():
            Board.paste(
                Radio_Button,
                (self.BOARD_FREQUENCY_POS_WIDTH[Frequency], 215 + round(Gain) * -20),
                Radio_Button,
            )

        fp = io.BytesIO()
        Board.save(fp, format="png")
        fp.seek(0)

        return fp


def setup(Bot):
    Bot.add_cog(Equalizer(Bot))
