import discord
import yaml
from discord.ext import commands
from discord import app_commands


bot_config_loc = "C:/Users/JuJin/Desktop/coin/discord_bot/config.yaml"
trading_config_loc = "C:/Users/JuJin/Desktop/coin/Auto_trading/config.yaml"
trading_data_loc = "C:/Users/JuJin/Desktop/coin/Auto_trading/data.yaml"
status_loc = "C:/Users/JuJin/Desktop/coin/bridge/status/"

class setting(commands.Cog):


    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    
    
    # @commands.command(name = "자금설정")
    # async def set_money(self,ctx,money_num):
    #     arg = float(money_num)
    #     with open(trading_config_loc, encoding='utf-8') as f:
    #         trading_config_data = yaml.load(f, Loader=yaml.FullLoader)

    #     embed=discord.Embed(title="기본설정 | 자금설정", color=0x90EE90)
    #     embed.add_field(name=f"변경 전", value=f"{trading_config_data['funds']}", inline=True)
    #     embed.add_field(name=f"변경 후", value=f"{arg}", inline=True)

    #     mes = await ctx.send(embed = embed)

    #     a = trading_config_data['funds']
    #     trading_config_data['funds'] = arg
    #     with open(trading_data_loc, encoding='utf-8') as f:
    #         trading_data_data = yaml.load(f, Loader=yaml.FullLoader)

    #     for fdd in trading_data_data["cell_funds"]:
    #         trading_data_data["cell_funds"][fdd] = arg / 5

    #     for i in range(0,5):
    #         with open(f"{status_loc}/cell {i}.yaml", encoding='utf-8') as f:
    #             cell_data = yaml.load(f, Loader=yaml.FullLoader)
    #         cell_data["funds"] = arg / 5
    #         cell_data["cell_status"] = "waiting..."
    #         cell_data["sell_price"] = 0.0
    #         cell_data["cut_sell_price"] = 0.0

    #         with open(f"{status_loc}/cell {i}.yaml", 'w', encoding = 'utf-8') as outfile:
    #             yaml.dump(cell_data, outfile, indent = 4, allow_unicode = True)



    #     embed=discord.Embed(title="기본설정 | 자금설정", color=0x90EE90)
    #     embed.add_field(name=f"변경 완료", value=f"자금이 ``{a}`` ---> ``{arg}``로 변경되었습니다.", inline=True)
    #     await mes.edit(embed = embed,components = [])

    #     with open(trading_config_loc, 'w', encoding = 'utf-8') as outfile:
    #         yaml.dump(trading_config_data, outfile, indent = 4, allow_unicode = True)
    #     with open(trading_data_loc, 'w', encoding = 'utf-8') as outfile:
    #         yaml.dump(trading_data_data, outfile, indent = 4, allow_unicode = True)
    

    
    @app_commands.command(name = "코인설정", description="거래할 코인을 입력해주세요. 예) KRW-BTC")
    async def set_coin(self, interaction: discord.Interaction, coin_symbol: str) -> None:
        with open(trading_config_loc, encoding='utf-8') as f:
            trading_config_data = yaml.load(f, Loader=yaml.FullLoader)

        a = trading_config_data['coin_type']
        trading_config_data['coin_type'] = coin_symbol

        embed=discord.Embed(title="기본설정 | 코인설정", color=0x90EE90)
        embed.add_field(name=f"변경 완료", value=f"코인이 ``{a}`` ---> ``{coin_symbol}``로 변경되었습니다.", inline=True)
        await interaction.response.send_message(embed = embed)
        with open(trading_config_loc, 'w', encoding = 'utf-8') as outfile:
            yaml.dump(trading_config_data, outfile, indent = 4, allow_unicode = True)



    @app_commands.command(name= "구매시작", description="코인구매를 시작합니다.")
    async def start_trading(self, interaction: discord.Interaction) -> None:
        with open(trading_config_loc, encoding='utf-8') as f:
            trading_config_data = yaml.load(f, Loader=yaml.FullLoader)


        trading_config_data['active'] = True

        embed=discord.Embed(title="구매중지", description = "구매가 시작되었습니다.", color=0x90EE90)
        embed.add_field(name=f"현재상태", value=f"active: ``{trading_config_data['active']}``", inline=True)
        await interaction.response.send_message(embed = embed)
        with open(trading_config_loc, 'w', encoding = 'utf-8') as outfile:
            yaml.dump(trading_config_data, outfile, indent = 4, allow_unicode = True)





    @app_commands.command(name = "구매중지", description = "코인구매를 중지합니다. 단, 판매는 계속됩니다.")
    async def stop_trading(self, interaction: discord.Interaction) -> None:
        with open(trading_config_loc, encoding='utf-8') as f:
            trading_config_data = yaml.load(f, Loader=yaml.FullLoader)


        trading_config_data['active'] = False

        embed=discord.Embed(title="구매중지", description = "구매가 중지되었습니다.", color=0x90EE90)
        embed.add_field(name=f"현재상태", value=f"{trading_config_data['active']}", inline=True)
        await interaction.response.send_message(embed = embed)
        with open(trading_config_loc, 'w', encoding = 'utf-8') as outfile:
            yaml.dump(trading_config_data, outfile, indent = 4, allow_unicode = True)







async def setup(client: commands.Bot) -> None:
    await client.add_cog(setting(client), guilds=[discord.Object(id = 919273060710879273)])