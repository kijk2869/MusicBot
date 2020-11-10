import sys

sys.path.append(r"C:\\Users\\mary\\Desktop\\GitHub\\discodo")

from discord.ext import commands
import discodo
import cogs

print(discodo.__version__)


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.Audio = discodo.DPYClient(self)

        cogs.load(self)
        self.load_extension("jishaku")


if __name__ == "__main__":
    bot = Bot(command_prefix=">>>")
    bot.Audio.register_node(
        "localhost", 8000, password="hellodiscodo", region="Local-01"
    )
    bot.Audio.register_node(
        "193.123.232.191", 8000, password="hellodiscodo", region="Oracle-01"
    )
    bot.run("NDE1NDAxNDM3MjQ2NTIxMzQ0.WovGvA.nvUOnQXzvGUVpC5TEwnD6wUtHlM")
