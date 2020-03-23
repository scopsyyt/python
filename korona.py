import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import bs4
import aiohttp
import datetime

client = commands.Bot(command_prefix='')

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

client.run("Njc3ODkwNTg2NjY1MTU2NjA5.Xnj13A.LZpCvFNdS4QP7bjoeWaF0Q8iGjE")
