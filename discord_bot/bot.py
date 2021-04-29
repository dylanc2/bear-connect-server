import discord
from discord.ext import commands, ipc
import json

TOKEN = "ODMxOTMzMDExNjAzMjI2NjM0.YHcb_g.UFByVVscN-QJF9nRGdThp_v4oBw"
BEAR_CONNECT_GUILD_ID = 831950960086745108
TEST_CHANNEL_ID = 831950960086745110
TEST_CHANNEL_ID_2_PV =832022610031935548
class MyBot(commands.Bot):

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

		self.ipc = ipc.Server(self,secret_key = "BEAR_CONNECT_SECRET_KEY")
		self.guild = None
		self.channels = []
		self.channel_test = None
	async def on_ready(self):
		"""Called upon the READY event"""
		print("Bot is ready.")
		self.guild = await self.fetch_guild(BEAR_CONNECT_GUILD_ID)
		print(self.guild)
		print("Guild is ready")

		self.channels = await self.guild.fetch_channels()

	async def on_ipc_ready(self):
		"""Called upon the IPC Server being ready"""
		print("Ipc server is ready.")

	async def on_ipc_error(self, endpoint, error):
		"""Called upon an error being raised within an IPC route"""
		print(endpoint, "raised", error)


	def my_get_guild(self):
		return self.guild

my_bot = MyBot(command_prefix = ">", intents = discord.Intents.default())


# bot async function to support home end point call
@my_bot.ipc.route()
async def get_member_count(data):
    guild = my_bot.get_guild(
        data.guild_id
    )  # get the guild object using parsed guild_id

    return guild.member_count + 1 # return the member count to the client

# bot async function to support get invite call
@my_bot.ipc.route()
async def get_invite(data):
	result = None
	print(my_bot.guild.name)
	my_channel = await my_bot.fetch_channel(data.channel_id)
	print("Channel Fetch attempt 1: ", my_channel)

	if my_channel:
		invites = await my_channel.invites()
		if len(invites) < 1:
			invite = await my_channel.create_invite()
			result = invite.url
		else:
			result = invites[0].url
	return result

# bot async function to support get members call
@my_bot.ipc.route()
async def get_channel_member(data):
	result = 0
	print(my_bot.guild.name)
	my_channel = await my_bot.fetch_channel(data.channel_id)
	print("Channel Fetch attempt 1: ", my_channel)

	if my_channel:
		result = len(my_channel.members)
	return result

# bot async function to create channel (WILL MAKE CHANGE TO MAKE IT PRIVATE)
@my_bot.ipc.route()
async def create_channel(data):
	print("function invoked")
	data = {"channel_id": None,
			"channel_invite": None}

	my_channel = await my_bot.guild.create_text_channel('cool-channel')
	invite = await my_channel.create_invite()

	print("channel Created")
	try:
		data['channel_id'] = my_channel.id
		data['channel_invite'] = invite.url
	except:
		print("Channel creation error")

	print(data)

	return json.dumps(data)

@my_bot.command()
async def hi(ctx):
	await ctx.send("hello")

my_bot.ipc.start()
my_bot.run(TOKEN)
