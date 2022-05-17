import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext  
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
import datetime
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
import asyncio
from discord.ext import tasks
from itertools import cycle
import random



cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'firebaseurl'
})


bot = commands.Bot(command_prefix=['?'], intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
  print('로딩완료')
  await bot.change_presence(activity=discord.Game("/docs"))


@bot.event
async def on_component(ctx):
  id = ctx.custom_id

  if id == 'verify':
    dir = db.reference(f'{ctx.guild.id}/certify')
    role = dir.get()
    print(role)
    roles = discord.utils.get(ctx.guild.roles, name=f"{role}")
    print(roles)
    await ctx.author.add_roles(roles)
    embed = discord.Embed(
      title="✅Certify success(인증 성공!)", 
      description=f"<@&{roles.id}> granted successfully.", 
      color=0x1DDB16,
    )
    await ctx.reply(embed=embed, hidden = True)















@slash.slash(name="button_certify",description="Send message and button for certify.(버튼형 인증메세지를 보냅니다.)")
async def buttoncertify(ctx, msg : str, add_role : discord.Role, button_msg : str = 'verify'):
  dir = db.reference(f'{ctx.guild.id}/channel')
  id = dir.get()
  if id == None:
    embed = discord.Embed(
      title="❌ERROR(채널을 먼저 설정해주세요!)", 
      description=f"Please set up your channel first!", 
      color=0xFF0000,
    )
    await ctx.reply(embed=embed, hidden = True)
    return None

  dir = db.reference(f'{ctx.guild.id}')
  dir.update({'certify' : f"{add_role.name}"})
  channel = bot.get_channel(int(id))
  buttons = [
    create_button(style=ButtonStyle.green, label=button_msg, custom_id = 'verify')
  ]
  action_row = create_actionrow(*buttons)
  await channel.send(msg, components=[action_row])
  embed = discord.Embed(
      title="✅Send success(보내기 성공!)", 
      description=f"Message successfully sent to <#{int(id)}>", 
      color=0x1DDB16,
    )
  await ctx.reply(embed=embed)

@slash.slash(name="set_channel",description="Set the channel to send the certify message(인증메세지를 보낼 채널을 설정합니다)")
async def setchannel(ctx, channel : discord.TextChannel):
  dir = db.reference(f'{ctx.guild.id}')
  dir.update({'channel' : f"{channel.id}"})
  embed = discord.Embed(
      title="📌Set channel(채널설정)", 
      description=f"Set to send messages to <#{channel.id}>", 
      color=0xF2CB61,
    )
  await ctx.send(embed=embed)
  
bot.run(token)
