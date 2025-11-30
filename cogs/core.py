import sys
from discord.ext import commands

class Core(commands.Cog):
    """ Basic commands """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello", help="Hi :)")
    async def hello(self, ctx):
        await ctx.send(f"Hi {ctx.author.mention}")

    @commands.command(name="ping", help="Check latency")
    async def ping(self, ctx):
        self.latency = round(self.bot.latency * 1000, 2)
        await self.bot.main_channel.send(f"pong! {self.latency}ms")
        self.bot.logger.info(f"{ctx.author} ping: {self.latency}ms")

    @commands.command(name="shutdown", help="Shutdown the server remotely")
    async def shutdown(self, ctx):
        await ctx.send("Ok good night :pleading_face:")
        # TODO this doesn't seem to cut it
        await self.bot.close()
        await sys.exit()

async def setup(bot):
    await bot.add_cog(Core(bot))