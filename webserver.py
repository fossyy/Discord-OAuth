from quart import Quart, redirect, url_for, render_template, session
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext import ipc

app = Quart(__name__)
ipc = ipc.Client(secret_key="test") #Make sure its was the same with secret_key in ipc.py

app.secret_key = b"JustaRandomText"

app.config["DISCORD_CLIENT_ID"] = 123 #Client Id Here
app.config["DISCORD_CLIENT_SECRET"] = "<CLIENT_SECRET_HERE>" #Client Secret here
app.config["DISCORD_REDIRECT_URI"] = "http://localhost:5000/callback" #Redirect url here (Make sure the port you are useing is correct)
app.config["DISCORD_BOT_TOKEN"] = "<BOT_TOKEN_HERE>" #PUT YOUR BOT TOKEN HERE

discord = DiscordOAuth2Session(app)

@app.route('/')
async def index():
    guildCount = await ipc.request("get_guild_count")

    try:
        userName = await discord.fetch_user()
    except:
        userName = None

    return await render_template('index.html', authorized = await discord.authorized, userName=userName, guildCount=guildCount)

@app.route("/login/")
async def login():
    return await discord.create_session()
    
@app.route("/logout")
async def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/callback")
async def callback():
    try:
        await discord.callback()
    except :
        return redirect(url_for("login"))

    return redirect(url_for("index"))

@app.route("/dashboard/")
async def dashboard():
    if not await discord.authorized:
        return redirect(url_for("login")) 

    userGuild = await discord.fetch_guilds()
    botGuild = await ipc.request('get_guild_ids')

    guildFinal = []

    for guild in userGuild:
        if guild.permissions.administrator:
            guildFinal.append(guild)

    return await render_template("dashboard.html", GuildList= guildFinal) 

@app.route("/dashboard/<int:guild_id>")
async def dashboard_server(guild_id):
	if not await discord.authorized:
		return redirect(url_for("index")) 

	guild = await ipc.request("get_guild", guild_id = guild_id)
	if guild is None:
		return redirect(f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=8&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')
	return guild["name"]

@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login"))

    


if __name__ == "__main__":
    app.run()