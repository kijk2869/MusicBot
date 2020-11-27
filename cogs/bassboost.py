from discord.ext import commands

from . import check_voice_connection


class Bassboost(commands.Cog):
    def __init__(self, Bot) -> None:
        self.Bot = Bot

    @commands.command(name="bassboost", aliases=["베이스부스트", "bb"])
    @commands.check(check_voice_connection)
    async def bassboost(self, ctx, value: int = None) -> None:
        VC = self.Bot.Audio.getVC(ctx.guild.id)
        State: dict = await VC.getState()

        if "bass" in State["options"]["filter"]:
            boostValue = float(
                dict(
                    map(
                        lambda x: x.split("="),
                        State["options"]["filter"]["bass"].split(":"),
                    ),
                ).get("gain", 0.0)
            )
        else:
            boostValue = 0.0

        if value is None:
            return await ctx.send(
                f"> 🎛️  **베이스 부스트 효과**\n> 🔊  현재 값: **{f'{round(boostValue / 7.5 * 100)}%' if boostValue else '설정되지 않음'}**"
            )

        if value > 500:
            return await ctx.send("❎  매개 변수는 **200%** 보다 클 수 없어요!")
        elif value < 0:
            return await ctx.send("❎ 매개 변수는 **0%** 보다 작을수 없어요!")

        boostValue = round(value / 100 * 7.5, 1)

        mergedFilter = State["options"]["filter"]
        if boostValue:
            mergedFilter["bass"] = f"gain={boostValue}"
        elif "bass" in mergedFilter:
            del mergedFilter["bass"]

        await VC.setFilter(mergedFilter)

        return await ctx.send(
            f"""
            > 🎛️  **베이스 부스트 효과**
            > 🔊  현재 값: **{f'{value}%' if value else '설정되지 않음'}**
            > 💡  `노래 효과는 적용되는 데에 5초에서 10초 정도 시간이 걸릴 수 있어요!`
            """
        )


def setup(Bot):
    Bot.add_cog(Bassboost(Bot))
