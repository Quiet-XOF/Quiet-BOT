import asyncio
import logging
import secrets
from bot.quietbot import QuietBot


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    bot = QuietBot()
    await bot.load_cogs()
    await bot.start(secrets.token)

if __name__ == "__main__":
    asyncio.run(main())