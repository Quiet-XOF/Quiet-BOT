import asyncio
import discord
import json
import os
import subprocess
from discord.ext import commands


class Scrape(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitter_users_file = "twitter_users.json"
        self.twitter_users = self.load_users(self.twitter_users_file)
        
    def load_users(self, filename):
        try:
            if os.path.exists(filename):
                with open(filename) as file:
                    data = json.load(file)
                    return data.get("users", [])
            else:
                return []
        except (json.JSONDecodeError, KeyError) as e:
            self.bot.logger.error(f"{e}")
            return []
    def save_users(self, filename, userlist):
        try:
            with open(filename, "w") as file:
                json.dump({"users": userlist}, file, indent=4)
        except Exception as e:
            self.bot.logger.error(f"{e}")

    @commands.command(name="addtw")
    async def addtw(self, ctx, user):
        if user not in self.twitter_users:
            self.twitter_users.append(user)
            self.save_users(self.twitter_users_file, self.twitter_users)
            await self.bot.main_channel.send(f":white_check_mark: {user} was added.")
        else:
            await self.bot.main_channel.send(f":x: {user} was already in list.")

    @commands.command(name="rmtw")
    async def rmtw(self, ctx, user):
        if user in self.twitter_users:
            self.twitter_users.remove(user)
            self.save_users(self.twitter_users_file, self.twitter_users)
            await self.bot.main_channel.send(f":white_check_mark: {user} was removed.")
        else:
            await self.bot.main_channel.send(f":x: {user} was not in list.")

    @commands.command(name="dltw", help="Use gallery-dl to scrape images")
    async def dltw(self, ctx, arg=None):
        download_count = 0 
        error_count = 0    
       
        async def scrape_user(user):
            try:
                result = await asyncio.create_subprocess_exec(
                    "timeout", "1h",
                    "gallery-dl", 
                    "--dest", "/mnt/sdb1/gallery-dl/",#"gallery-dl/",
                    "--sleep", "1.5-2.0",
                    "--abort", "5",
                    "--cookies-from-browser", "firefox",
                    f"https://twitter.com/{user}",
                    "--write-info-json",
                    "--download-archive", "download-archive",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                output, error = await result.communicate()
                output = output.decode("utf-8").strip()
                error = error.decode("utf-8").strip()
                self.bot.logger.info(output)
                await result.wait()
                return output, error
            except Exception as e:
                #self.logger.info(f"Error: {e}")
                await self.bot.error_channel.send(f"`Error: {e}`")

        users = [arg] if arg else self.twitter_users
        if not users:
            await self.bot.main_channel.send("No users to scrape.")
            return

        await self.bot.main_channel.send("Beginning scrape... :hourglass_flowing_sand:")

        for user in users:
            self.bot.logger.info(f"Scraping {user}")
            output, error = await scrape_user(user)
            if "error" in error:
                self.bot.logger.info(f"{user}: {error}")
                await self.bot.error_channel.send(f"`{user}: {error}`")
                error_count += 1
            if output:
                for line in output.splitlines():
                    line = line.strip()
                    if line.startswith("/mnt/sdb1/gallery-dl/"):
                        try:
                            filepath = os.path.abspath(line)
                            filename = os.path.basename(filepath)
                            await self.bot.download_channel.send(
                                f"[{user}](https://twitter.com{user})",
                                file=discord.File(filepath)
                            )
                        except Exception as e:
                            await self.bot.error_channel.send(f"`Error: {e}`")
                        download_count += 1

        await self.bot.main_channel.send("Scraping complete. :white_check_mark:")
        if download_count:
            await self.bot.main_channel.send(f"There were {download_count} downloads. :chart_with_upwards_trend:")
        if error_count:
            await self.bot.main_channel.send(f"There were {error_count} errors. :chart_with_downwards_trend:")

    async def get_users(self, filename):
        # Simple: open the provided filename in the current working directory
        if not os.path.exists(filename):
            return []
        with open(filename, "r", encoding="utf-8") as file:
            return file.read().splitlines()
        #if not os.path.exists(filename):
        #    await self.bot.error_channel.send("File twitter.txt not found.")
        #    return
        #else:
        #    with open(filename, "r") as file:
        #        return file.read().splitlines()

async def setup(bot):
    await bot.add_cog(Scrape(bot))