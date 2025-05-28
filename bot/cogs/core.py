from discord.ext import commands


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Check latency.")
    async def ping(self, ctx):
        await ctx.send(f"pong! {round(self.bot.latency * 1000, 2)}ms")

    @commands.command(name="shutdown", help="Shutdown the server remotely.")
    async def shutdown(self, ctx):
        await ctx.send("Ok good night :pleading_face:")
        # TODO this doesn't seem to cut it
        await bot.close()

async def setup(bot):
    await bot.add_cog(Core(bot))