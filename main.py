import asyncio
import json
import logging
from bot.quietbot import QuietBot


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    with open("secrets.json", "r") as file:
        secrets = json.load(file)
    
    bot = QuietBot()
    await bot.load_cogs()
    await bot.start(secrets["token"])

if __name__ == "__main__":
    asyncio.run(main())