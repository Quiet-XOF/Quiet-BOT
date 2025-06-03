import asyncio
import json
import logging
import sys
from bot.quietbot import QuietBot


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    
    try:
        with open("secrets.json", "r") as file:
            secrets = json.load(file)
    except Exception as e:
        print("The file \"secrets.json\" doesn't exist.")
        print("Please inspect the file and add your information.")
        print("Creating file...")
        default = {"token" : None, "twit_user" : None, "twit_pass" : None}
        with open("secrets.json", "w") as file:
            json.dump(default, file, indent=4)
        sys.exit()
    
    bot = QuietBot()
    await bot.load_cogs()
    await bot.start(secrets["token"])

if __name__ == "__main__":
    asyncio.run(main())