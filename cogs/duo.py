import discord
from discord.ext import tasks, commands
import random
import json

setupfile = open("load/setup.json", "r")
setupdict = json.loads(setupfile.read())
setupfile.close()

hootloc = "load/duo.json"

class Hooty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.percent = 85

        hootfile = open(hootloc, "r")
        self.hootdict = json.loads(hootfile.read())
        hootfile.close()
        self.hoot_messages = self.hootdict["hoot-messages"]
        self.languages = self.hootdict["languages"]


    def commit(self):
        hootfile = open(hootloc, "w+")
        self.hootdict["hoot-messages"] = self.hoot_messages
        json.dump(self.hootdict, hootfile)
        hootfile.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if message.channel.category_id in setupdict["hooty-not-allowed-categories"]: return
        if message.channel.id == 827004123031142411: return
        
        generate = random.randint(1,100)
        if generate <= self.percent:
            hoot_message_num = random.randint(0,len(self.hoot_messages)-1)
            await message.channel.send(self.hoot_messages[hoot_message_num])
	
    @commands.command(name='hoot-percent', help="Change how often Duo hoots")
    @commands.has_role(setupdict["roles"]["resident"])
    async def hoot_percent(self, ctx, percent: int):
        if percent > 100 or percent < 0:
            await ctx.send("Invalid percentage.")
        else:
            self.percent = percent
            await ctx.send(f"You have changed Duo's hoot percentage to {percent}.")

    @commands.command(name='hoot', help="Hoot")
    async def hoot(self, ctx):
        language_num = int(random.randint(0,len(self.languages)-1))
        await ctx.send(f"It's time for your {self.languages[language_num]} lesson.")

    @commands.command(name='add-hoot', help="Add a hoot message sent by Duo")
    async def add_hoot(self, ctx, *, hoot_message: str):
        if hoot_message in self.hoot_messages:
            await ctx.send("This message is already a hoot message.")
        else:
            self.hoot_messages.append(hoot_message)
            self.commit()
            await ctx.send("You have added a hoot message.")

    @commands.command(name='remove-hoot', help="Remove a hoot message sent by Duo")
    async def remove_hoot(self, ctx, *, hoot_message: str):
        if hoot_message not in self.hoot_messages:
            await ctx.send("This message is not a valid hoot message.")
        else:
            self.hoot_messages.remove(hoot_message)
            self.commit()
            await ctx.send("You have removed a hoot message.")

    @commands.command(name='view-hoots', help="List all hoot messages")
    async def view_hoots(self, ctx):
        hoot_messages_str = ""
        for message in self.hoot_messages:
            hoot_messages_str += f"{message}\n"
        await ctx.send(hoot_messages_str)

def setup(bot):
    bot.add_cog(Hooty(bot))