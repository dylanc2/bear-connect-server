import discord
from discord.ext import commands
from discord.utils import get
from quart import Quart, request
from coolname import generate_slug
import json

BEAR_CONNECT_GUILD_ID = 831950960086745108
CATEGORY_CHANNEL_ID = 831955925186510929
TEST_CHANNEL_ID_2_PV = 832022610031935548
TOKEN = "ODMxOTMzMDExNjAzMjI2NjM0.YHcb_g.UFByVVscN-QJF9nRGdThp_v4oBw"


class MyBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.guild = None
        self.channels = []
        self.channel_test = None
        self.category_channel = None

    async def on_ready(self):
        """Called upon the READY event"""
        print("Bot is ready.")
        self.guild = await self.fetch_guild(BEAR_CONNECT_GUILD_ID)
        print(self.guild)
        print("Guild is ready")
        self.channels = await self.guild.fetch_channels()
        self.category_channel = await bot.fetch_channel(CATEGORY_CHANNEL_ID)

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
        return str("Unsuccessful Fetch"), 300

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
@app.route("/create_channel", methods=['POST'])
async def create_channel():
    response = ""
    if request.method == 'POST':
        data = {"channel_id": None,
                "channel_invite": None}

        # private_member_role = get(bot.guild.roles, name="private_room_member")
        # print(private_member_role)
		#category_channel = get(bot.guild.channels, name="Private_study_groups")
        # overwrites = {bot.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        #               private_member_role: discord.PermissionOverwrite(read_messages=True)}

        stud_room_name = generate_slug(3) + "-study-group"
        my_channel = await bot.guild.create_text_channel(stud_room_name, category = bot.category_channel)
        invite = await my_channel.create_invite()
        print("channel Created")
        try:
            data['channel_id'] = my_channel.id
            data['channel_invite'] = invite.url
        except:
            print("Channel creation error")
        return json.dumps(data), 200


bot.loop.create_task(app.run_task(host='0.0.0.0'))

bot.run(TOKEN)
