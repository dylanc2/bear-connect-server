from quart import Quart,request
from discord.ext import ipc

BEAR_CONNECT_GUILD_ID = 831950960086745108

app = Quart(__name__)
ipc_client = ipc.Client(secret_key = "BEAR_CONNECT_SECRET_KEY")

# to test home route
@app.route("/")
async def home():
	member_count = await ipc_client.request("get_member_count", guild_id=BEAR_CONNECT_GUILD_ID)  # get the member count of server with ID 12345678
	return str(member_count)

# END point to get channel invite
@app.route("/get_invite/<int:channel_id>", methods = ['GET'])
async def get_invite(channel_id):
	invite_str = await ipc_client.request("get_invite", channel_id=channel_id)
	if not invite_str:
		return "No Invite Found", 400
	else:
		return invite_str, 200

# END point to get visible members in channel
@app.route("/get_member/<int:channel_id>", methods = ['GET'])
async def get_member(channel_id):
	response = 0
	response = await ipc_client.request("get_channel_member", channel_id=channel_id)
	return str(response), 200

# END point to create a new channel
@app.route("/create_channel", methods = ['POST'])
async def create_channel():
	response = ""
	if request.method == 'POST':
		response = await ipc_client.request("create_channel")
	return response, 200

if __name__ == "__main__":
	app.run(debug=True)
