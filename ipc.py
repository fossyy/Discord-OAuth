import discord
from discord.ext import commands, ipc


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key="test")

    async def on_ready(self):
        await bot.ipc.start()
        print("Bot is ready.")

    async def on_ipc_ready(self):
        print("IPC is ready.")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)


bot = MyBot(command_prefix=":;,.<>!!@@###!#!_-", intents=discord.Intents.all())


@bot.ipc.route()
async def get_member_count(data):
    guild = bot.get_guild(data.guild_id) 
    return guild.member_count 

@bot.ipc.route()
async def get_guild_count(data):
    return len(bot.guilds)

@bot.ipc.route()
async def get_guild_ids(data):
    final = []
    for guild in bot.guilds:
        final.append(guild.id)
    return final

@bot.ipc.route()
async def get_guild(data):
	guild = bot.get_guild(data.guild_id)
	if guild is None: return None

	guild_data = {
		"name": guild.name,
		"id": guild.id,
		"prefix" : "?"
	}

	return guild_data

if __name__ == "__main__":
    bot.run("<BOT_TOKEN_HERE>")