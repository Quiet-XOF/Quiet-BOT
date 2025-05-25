import secrets
from bot.quietbot import QuietBot
import asyncio


async def main():
    bot = QuietBot()
    await bot.load_cogs()
    await bot.start(secrets.token)

if __name__ == "__main__":
    asyncio.run(main())