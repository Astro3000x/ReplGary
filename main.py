import os
import discord
import bs4
import requests
from discord.ext import commands
import asyncio
from replit import db
import socket

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for !commands"))
@bot.command()
async def online(ctx):
  await ctx.reply("Online!")

@bot.command()
async def status(ctx):
  

  result = requests.get("https://status.replit.com")
  inner = str(result.content)
  final = inner.split("Don't agree with this?")
  #print(inner)
  with open('readme.txt', 'w') as f:
    f.write(final[0])
  if "All systems are go" in final[0]:
    await ctx.reply("All systems are go!")
  elif "Evaluation API" in final[0]:
    await ctx.reply("Evaluation API is degraded or down.")
  elif "Static Hosting" in final[0]:
    await ctx.reply("Static Hosting (Static HTML Repls) Offline")
  elif "Dynamic Hosting" in final[0]:
    await ctx.reply("Dynamic Hosting (HTTP(S) access to your Repl's exposed ports) Offline")
  elif "Replit Database" in final[0]:
    await ctx.reply("ReplIt Database Offline")
  elif "Repl DNS" in final[0]:
    await ctx.reply("Repl DNS (.repl.co subdomains) Offline")
  elif "Always-On" in final[0]:
    await ctx.reply("Always On Infastructure Offline")
  elif "replit.com" in final[0]:
    await ctx.reply("Main replit.com site offline")
  elif "docs.replit.com" in final[0]:
    await ctx.reply("Replit Doumentation Page Offline")
  elif "blog.replit.com" in final[0]:
    await ctx.reply("Replit Blog Page Offline")
  else:
    await ctx.replt("Some systems offline.")

@bot.command()
async def link(ctx, username: str):
  result = requests.get(f"https://replit.com/@{username}/")
  final = str(result.content)
  
  uid = ctx.message.author.id
  
  user = ctx.message.author
  userid = ctx.message.author.id
  if str(user) in final:
    
    db[user] = username
    db['<@'+str(uid)+'>'] = username
    await ctx.reply(f"Linked to @{username}! {user}")
  else:
    await ctx.send("ReplIt Account Does Not Contain A Linked Discord Account or has Incorrect Info, Use !helplink for more info")

@bot.command()
async def echo(ctx, msg : str):
  await ctx.send(msg)
@bot.command()
async def ping(ctx, site : str):
  if "https://" in site:
    ff = site.split("https://")[0]
    dd = ff.split("/")[0]
  else:
    dd = site
  await ctx.send(socket.gethostbyname(dd))
  
@bot.command()
async def cmd(ctx):
  embed=discord.Embed(title="Cmd Commands:", description="Ping: Ping a website\nEcho: Echo a message", color=0xFF5733)
  await ctx.send(embed=embed)
@bot.command()
async def commands(ctx):
  embed=discord.Embed(title="ReplGary Commands:", description="Prefix: !\nWhois: Search a User On Replit\nStatus: Get The Status Of The Replit Site\nLink link your repl account to discord account\nLinkHelp: More Info For Linking\nUserepl: Find A Discord Users Linked ReplIt Account\nThank: Thank somebody for helping you with code\nCmd: Get Cmd Commands", color=0xFF5733)
  await ctx.send(embed=embed)

@bot.command()
async def whois(ctx, user: str):
  result = requests.get(f"https://replit.com/@{user}")
  inner = str(result.content)
  final = inner.split('<script id="__NEXT_DATA__" type="application/json">')
  
  if str(result) == "<Response [404]>":
    await ctx.reply("User Does Not Exist")
  else:
    if '<span class="jsx-3743526e8ffb5016 user-roles-label hacker">hacker</span>' in final[0]:
      hacker = ", Has Hacker Plan"
    else:
      hacker = ", No Hacker Plan"
    if '<span title="Helps moderate Repl Talk by wielding the power of the banhammer" class="jsx-3743526e8ffb5016 user-roles-label moderator">moderator</span>' in final[0]:
      mod = ", Is a mod"
    else:
      mod = ", Is not a mod"
    if '<span title="Creates awesome tutorials and templates for Replit" class="jsx-3743526e8ffb5016 user-roles-label content-creator">content creator</span>' in final[0]:
      cc = ", Is a Content Creator"
    else:
      cc = ", Not a content creator"
    await ctx.reply(f"{user}{hacker}{mod}{cc}. Source: https://replit.com/@{user}")
@bot.command()
async def helplink(ctx):
  await ctx.send("Under avatar on profile page click edit and add discord username and tag: https://cdn.discordapp.com/attachments/870417952153944115/971981051482214400/Screen_Shot_2022-05-05_at_8.43.46_PM.png https://cdn.discordapp.com/attachments/870417952153944115/971981051834544228/Screen_Shot_2022-05-05_at_8.44.20_PM.png")
@bot.command()
async def userepl(ctx, p : str):
  if p in db.keys():
    await ctx.send(f"https://replit.com/@{db[p]}")
  else:
    await ctx.send("User Does Not Have Repl Account Linked")
@bot.command()
async def thank(ctx, userthank : str):
  user = ctx.message.author.id
  next = userthank.split("@")
  final = next[1].split(">")
  ff = final[0]

  if ff != str(user):
    if ff in db.keys():
      db[ff] += 1
    else:
      db[ff] = 1
    await ctx.send(f"🎉 Thanks for helping <@{user}>, {userthank}!")
  else:
    await ctx.send("You can't thank yourself!")

@bot.command()
async def awards(ctx):
  await ctx.reply(f"You Have {db[str(ctx.message.author.id)]} Awards For Helping People")
@bot.command()
async def experience(ctx, user : str):
  next = user.split("@")
  final = next[1].split(">")
  ff = final[0]
  await ctx.reply(f"<@{ff}> has {db[str(ff)]} Awards For Helping People")
token = os.environ["TOKEN"]
bot.run(token)