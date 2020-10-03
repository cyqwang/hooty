# 1
import discord
from discord.ext import tasks, commands

import json
setupfile = open("load/setup.json", "r")
setupdict = json.loads(setupfile.read())
setupfile.close()

class General(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="load")
	@commands.is_owner()
	async def load(self, ctx, cog:str):
		try:
			self.bot.load_extension(cog)
		except Exception as e:
			await ctx.send(f"Could not load {cog}.")
			return
		await ctx.send(f"{cog} loaded.")

	@commands.command(name="unload")
	@commands.is_owner()
	async def unload(self, ctx, cog:str):
		try:
			self.bot.unload_extension(cog)
		except Exception as e:
			await ctx.send(f"Could not unload {cog}.")
			return
		await ctx.send(f"{cog} unloaded.")

	@commands.command(name="reload")
	@commands.is_owner()
	async def reload(self, ctx, cog:str):
		try:
			self.bot.unload_extension(cog)
			self.bot.load_extension(cog)
		except Exception as e:
			await ctx.send(f"Could not reload {cog}.")
			return
		await ctx.send(f"{cog} reloaded.")

def setup(bot):
    bot.add_cog(General(bot))