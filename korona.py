import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import bs4
import aiohttp
import datetime

client = commands.Bot(command_prefix='s.')

print ("scop")
print ("ScoKramp betöltése...")

@client.event
async def on_ready():
	print ("A rendszer elindult!")

@client.command()
async def koronavirus(ctx):
    if ctx.author.bot:
        return
    loadmsg = await ctx.send("Kérlek várj...")
    async with aiohttp.ClientSession() as session:
        async with session.get("https://koronavirus.gov.hu") as r:
            resp = await r.text()
    import bs4
    soup = bs4.BeautifulSoup(resp, features="lxml")
    i = 0
    for price in soup.find_all('div', {"class": "diagram-a"}):
        i += 1
        if i == 1:
            fertozott = price.get_text()
            fertozott = fertozott.replace("""Fertőzött
igazoltan új koronavírussal fertőzöttek száma""", "")
            fertozott = " ".join(fertozott.split())
        elif i == 2:
            gyogyult = price.get_text()
            gyogyult = gyogyult.replace("""Gyógyult
új koronavírus-fertőzésből gyógyultak száma""", "")
            gyogyult = " ".join(gyogyult.split())
        elif i == 3:
            elhunyt = price.get_text()
            elhunyt = elhunyt.replace("""Elhunyt
új koronavírus-fertőzés miatt elhunytak száma""", "")
            elhunyt = " ".join(elhunyt.split())
        elif i == 4:
            karanten = price.get_text()
            karanten = karanten.replace("""Karanténban
új koronavírus gyanúja miatt elkülönítettek száma""", "")
            karanten = " ".join(karanten.split())
        elif i == 5:
            mintavetel = price.get_text()
            mintavetel = mintavetel.replace("""Mintavétel
akkreditált laboratóriumban vizsgált minták száma""", "")
            mintavetel = " ".join(mintavetel.split())
            break
    embed = discord.Embed(title="Koronavírus adatok", color=0x00ff00, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Fertőzöttek száma", value=f"**{fertozott}**")
    embed.add_field(name="Gyógyultak száma", value=f"**{gyogyult}**")
    embed.add_field(name="Elhunytak száma", value=f"**{elhunyt}**")
    embed.add_field(name="Karanténban lévők száma", value=f"**{karanten}**")
    embed.add_field(name="Mintavételek száma", value=f"**{mintavetel}**")
    embed.add_field(name="Forrás", value=f"[https://koronavirus.gov.hu](https://koronavirus.gov.hu)", inline=False)
    embed.set_author(name="koronavirus INFORMÁCIÓ", url="https://fightman01bot.ml/", icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text="FightMan01 bot - Koronavírus adatok", icon_url="https://fightman01bot.ml/favicon.png")
    await loadmsg.edit(content=None, embed=embed)

@client.command(pass_context=True)
async def gmail():
	embed = discord.Embed(
		title = 'Email cím',
		description = 'Ha valami hibát találnál a botban írd a lenti email címre',
		colour = discord.Colour.red()
	)
	embed.add_field(name='Személy neve', value='ScopsyYT', inline=False)
	embed.add_field(name='Email címe', value='scopsyscopsy@gmail.com', inline=False)
	embed.set_footer(text='KORONAVIRUS INFORMÁCIÓ')
	await client.say(embed=embed)

@client.command(pass_context=True)
async def say(ctx, *args):
	if ctx.message.author.server_permissions.manage_messages:
		mesg = ' '.join(args)
		await client.delete_message(ctx.message)
		return await client.say(mesg)
	else:
		return await client.say("❌ Nincs jogod használni! (Üzenetek kezelése)")

@client.command(pass_context=True)
async def avatar(ctx, member: discord.Member):
		u = member.avatar_url
		embed = discord.Embed(description="<@{}> Szép profil".format(member.id), colour=discord.Colour.gold())
		embed.set_image(url=u)
		await client.say(embed=embed)
@avatar.error
async def avatar_error(ctx, error):
	await client.say("Használd: avatar [@Member]")

@client.command(pass_context=True)
async def join(ctx):
	channel = ctx.message.author.voice.voice_channel
	await client.join_voice_channel(channel)



client.run("Njc3ODkwNTg2NjY1MTU2NjA5.XnirzA.lLtNxN-e5jVzcKrqkXQBjNL1fuI")
