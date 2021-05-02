import discord
from discord.ext import commands
from quart import Quart,request
import json

BEAR_CONNECT_GUILD_ID = 831950960086745108
TEST_CHANNEL_ID = 831950960086745110
TEST_CHANNEL_ID_2_PV = 832022610031935548
TOKEN = "ODMxOTMzMDExNjAzMjI2NjM0.YHcb_g.UFByVVscN-QJF9nRGdThp_v4oBw"


class MyBot(commands.Bot):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

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

	def my_get_guild(self):
		return self.guild


bot = MyBot(command_prefix=">", intents=discord.Intents.default())


# @bot.event
# async def on_ready():
#     print(f'{bot.user} has connected to Discord!')

@bot.command(name="hi")
async def hi_command(ctx):
    await ctx.channel.send("hello")

app = Quart(__name__)


@app.route("/")
async def hello():
    print(bot.guild)
    return "hello world"

# Get members in channel
@app.route("/get_member/<int:channel_id>", methods=['GET'])
async def get_member(channel_id):
    result = 0
    my_channel = await bot.fetch_channel(channel_id)
    try:
        if my_channel:
            result = len(my_channel.members)
        return str(result), 200
    except:
        return str("Unsuccessful Fetch"),300

# Get invite for the channel
@app.route("/get_invite/<int:channel_id>", methods=['GET'])
async def get_invite(channel_id):
	result = None
	my_channel = await bot.fetch_channel(channel_id)

	if my_channel:
		invites = await my_channel.invites()
		if len(invites) < 1:
			invite = await my_channel.create_invite()
			result = invite.url
		else:
			result = invites[0].url

	if not result:
		return "No Invite Found", 400
	else:
		return result, 200

# Get create new channel
@app.route("/create_channel", methods = ['POST'])
async def create_channel():
    response = ""
    if request.method == 'POST':
        data = {"channel_id": None,
                "channel_invite": None}
        my_channel = await bot.guild.create_text_channel('cool-channel_v2')
        invite = await my_channel.create_invite()
        print("channel Created")
        try:
            data['channel_id'] = my_channel.id
            data['channel_invite'] = invite.url
        except:
            print("Channel creation error")
        return json.dumps(data), 200



bot.loop.create_task(app.run_task(host = '0.0.0.0'))

bot.run(TOKEN)
