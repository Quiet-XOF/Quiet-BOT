import asyncio
import csv
import json
import os
import pandas
import random
import re
from discord.ext import commands


class Flashcards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.cards_file = os.path.join(os.path.dirname(__file__), "flashcards.json")
        with open(self.cards_file, "r") as file:
            self.flash_cards = json.load(file)
        self.category = list(self.flash_cards.keys())

        self.stats_file = os.path.join(os.path.dirname(__file__), "flashcard_stats.csv")
        self.headers = ["user_id", "category", "term", "incorrect"]
        self.stats = self.get_stats()

    def get_stats(self):
        if not os.path.exists(self.stats_file):
            with open(self.stats_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
                return self.headers
        else:
            with open(self.stats_file, newline="") as file:
                reader = csv.reader(file)
                return list(reader)

    @commands.command(name="quiz", help="Practice")
    async def quiz(self, ctx, arg=None):
        if arg not in self.category or not arg:
            await ctx.send(f"Current flash cards: {", ".join(self.category)}")
        else:
            while True:
                stats_df = pandas.DataFrame(data=self.stats)
                terms = self.flash_cards.get(arg, {})
                term, definition = random.choice(list(terms.items()))
                await ctx.send(term)

                def check(payload):
                    return payload.author == ctx.author and payload.channel == ctx.channel
                def normalize(string):
                    return re.sub(r"[^a-z0-9]", "", string.lower())

                try:
                    message = await self.bot.wait_for("message", timeout=120.0, check=check)
                    is_correct = normalize(message.content) == normalize(definition)

                    if is_correct:
                        await ctx.send("Correct!")
                    else:
                        await ctx.send(f"Incorrect!\n{definition}")

                except asyncio.TimeoutError:
                    await ctx.send("Time's up")
                    return
                except Exception as e:
                    await ctx.send(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(Flashcards(bot))