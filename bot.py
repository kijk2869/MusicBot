import discodo
from discord.ext import commands

import cogs

print(discodo.__version__)
import logging

logging.basicConfig(level=logging.INFO)
# logging.getLogger("discodo").setLevel(logging.DEBUG)


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.Audio = discodo.DPYClient(self)

        cogs.load(self)
        self.load_extension("jishaku")


if __name__ == "__main__":
    bot = Bot(command_prefix="!")
    bot.Audio.register_local_node()
    bot.run("Token")
