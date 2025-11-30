import asyncio
import discord
import os
import subprocess
from discord.ext import commands


class Scrape(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="addtw")
    async def addtw(ctx, arg):
        with open("twitter.txt", "r+") as file:
            lines = file.read().splitlines()
            if arg in lines:
                await self.bot.main_channel.send(f":x: {arg} was alredy in list.")
            else:
                file.write(arg + "\n")
                await self.bot.main_channel.send(f":white_check_mark: {arg} was added to the list.")

    @commands.command(name="gdl", help="Use gallery-dl to scrape images")
    async def gdl(self, ctx, arg=None):
        download_count = 0 
        error_count = 0    
        
        async def scrape_user(user):
            try:
                result = await asyncio.create_subprocess_exec(
                    "timeout", "1h",
                    "gallery-dl", 
                    "--dest", "gallery-dl/",
                    "--sleep", "1.5-2.0",
                    #"--abort", "5",
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
                await result.wait()
                return output, error
            except Exception as e:
                #self.logger.info(f"Error: {e}")
                await self.bot.error_channel.send(f"`Error: {e}`")

        users = [arg] if arg else await get_users("twitter.txt")
        if not users:
            await self.bot.main_channel.send("No users to scrape.")
            return

        await self.bot.main_channel.send("Beginning scrape... :hourglass_flowing_sand:")

        for user in users:
            output, error = await scrape_user(user)
            if "error" in error:
                self.bot.logger.info(f"{user}: {error}")
                await self.bot.error_channel.send(f"`{user}: {error}`")
                error_count += 1
            if output:
                for line in output.splitlines():
                    line = line.strip()
                    if line.startswith("gallery-dl/"):
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

    async def get_users(filename):
        if not os.path.exists(filename):
            await self.bot.error_channel.send("File twitter.txt not found.")
            return
        else:
            with open(filename, "r") as file:
                return file.read().splitlines()

async def setup(bot):
    await bot.add_cog(Scrape(bot))