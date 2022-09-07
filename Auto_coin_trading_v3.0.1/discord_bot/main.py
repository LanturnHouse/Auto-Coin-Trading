import discord
import yaml
import os
import time as t
from discord.ext import commands
from discord_components import *


#============  초기변수 설정  =================
config_loc = './config.yaml'
bot_manager = [339017884703653888,305234945629093898]


#============  intents  ================
intents = discord.Intents.all()
intents.members = True
intents.guilds = True




class aclient(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix= "!", intents=intents)
        
    
    async def setup_hook(self):
        with open(config_loc, encoding='utf-8') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)

        for filename in os.listdir("C:/Users/JuJin/Desktop/coin/discord_bot/Cogs"):
            if filename.endswith('.py'):
                print(f'Cog {filename[:-3]}이(가) Load 되었습니다.')
                aclient.load_extension(f'Cogs.{filename[:-3]}')
                    
        await aclient.tree.sync(guild=discord.Object(id = 919273060710879273))


    async def on_ready(self):
        print("\n\n")
        print(f'{aclient.user} Login!')
        with open(config_loc, encoding='utf-8') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
        await aclient.change_presence(status = discord.Status.online, activity = discord.Game(yaml_data['bot_status']))
        print('\n\n\n')
        print("====================================")
        print(f"starting time: {t.strftime('%Y-%m-%d %H:%M', t.localtime(t.time()))}")
        print("====================================\n")
        DiscordComponents(self)
        
        
'''
#============  봇 트리거  ================
bot = commands.Bot(command_prefix='!', intents=intents, help_command = None)

def status():
    print('\n\n\n')
    print("====================================")
    print(f"starting time: {t.strftime('%Y-%m-%d %H:%M', t.localtime(t.time()))}")
    print("====================================\n")
    DiscordComponents(bot)
'''


'''
#============  봇이 실행됬을때  ===========
@bot.event
async def on_ready():
    print("\n\n")
    print(f'{bot.user} Login!')
    with open(config_loc, encoding='utf-8') as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
    await bot.change_presence(status = discord.Status.online, activity = discord.Game(yaml_data['bot_status']))
    status()
'''



#=================  봇이 처음 켜질때 모든 Cogs 로드  =====================
with open(config_loc, encoding='utf-8') as f:
    yaml_data = yaml.load(f, Loader=yaml.FullLoader)

for filename in os.listdir("C:/Users/JuJin/Desktop/coin/discord_bot/Cogs"):
    if filename.endswith('.py'):
        print(f'Cog {filename[:-3]}이(가) Load 되었습니다.')
        aclient.load_extension(f'Cogs.{filename[:-3]}')


token = yaml_data['bot_token']

aclient.run(token)