import discord
import pyupbit
import yaml
import os
import time as t
from discord.ext import commands, tasks

path = "C:/Users/JuJin/Desktop/coin/bridge/status"
config_loc = "C:/Users/JuJin/Desktop/coin/discord_bot/config.yaml"
a_config_loc = "C:/Users/JuJin/Desktop/coin/auto_trading/config.yaml"
a_data_loc = "C:/Users/JuJin/Desktop/coin/auto_trading/data.yaml"
with open(config_loc, encoding='utf-8') as f:
    config_data = yaml.load(f, Loader=yaml.FullLoader)
    



def get_asking_price(now_price):
    """호가단위 게산"""
    if now_price < 0.1:
        return 0.0001
    elif now_price < 1:
        return 0.001
    elif now_price < 10:
        return 0.01
    elif now_price< 100:
        return 0.1
    elif now_price < 1000:
        return 1
    elif now_price < 10000:
        return 5
    elif now_price < 100000:
        return 10
    elif now_price < 500000:
        return 50
    elif now_price < 1000000:
        return 100
    elif now_price < 2000000:
        return 500
    else:
        return 1000





class status(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.status.start()
        self.loop_count = 0

    @tasks.loop(seconds = 5)
    async def status(self):
        try:
            with open(a_config_loc, encoding='utf-8') as f:
                a_config_data = yaml.load(f, Loader=yaml.FullLoader)
            with open(a_data_loc, encoding='utf-8') as f:
                a_data_data = yaml.load(f, Loader=yaml.FullLoader)
            with open(f'{path}/main_status.yaml' , encoding= 'utf-8') as f:
                status_data = yaml.load(f, Loader=yaml.FullLoader)
            now_price = pyupbit.get_current_price(a_config_data["coin_type"])
                
            if os.path.isfile(f"C:/Users/JuJin/Desktop/coin/bridge/program_active_check.txt"):
                self.loop_count = 0
                AT_program_active = ":green_circle:"
                os.remove(f"C:/Users/JuJin/Desktop/coin/bridge/program_active_check.txt")
                embed_color = 0x72ED00
                
            else:
                self.loop_count += 1
                AT_program_active = ":green_circle:"
                embed_color = 0x72ED00
            
            if self.loop_count >= 10:
                AT_program_active = ":red_circle:"
                embed_color = 0xFF3232
            
            embed=discord.Embed(title=f"자동거래 status         상태:    {AT_program_active}", description = 
            f"""```수익률
1일: {status_data['yield_t1-1']}%    7일: {status_data['yield_t1-7']}%    30일: {status_data['yield_t1-30']}%
1일: {status_data['yield_t2-1']}원    7일: {status_data['yield_t2-7']}원    30일: {status_data['yield_t2-30']}원

현재 가격: {now_price}
코인: {a_config_data['coin_type']}    호가: {get_asking_price(now_price)}    구매 활성화: {a_config_data['active']}
평단가: {float(a_data_data['avg_value'])}    tick: {a_data_data['tick']}    마지막 tick 가격: {a_data_data['tick_end_price']}```"""
            , color=embed_color)
            
            
            file_list = os.listdir(path)
            for file_name in file_list:
                if file_name.startswith("cell"):
                    with open(f"{path}/{file_name}", encoding='utf-8') as f:
                        cell_data = yaml.load(f, Loader=yaml.FullLoader)
                    cell_num = file_name.split(".")[0]


                    if cell_data["status"] == "s waiting...":
                        embed.add_field(name=f"{cell_num}", value=f'``cell 자금: {cell_data["funds"]}  ||  cell 상태: 판매 대기중...\n구매금액: {cell_data["buy_price"]}  ||  코인 갯수: {cell_data["buy_coin_num"]}``', inline=False)

                    elif cell_data["status"] == "b2 waiting...":
                        embed.add_field(name=f"{cell_num}", value=f'``cell 자금: {cell_data["funds"]}  ||  cell 상태: 구매오더 체결 대기중...\n구매금액: {cell_data["buy_price"]}  ||  코인 갯수: {cell_data["buy_coin_num"]}\n구매오더 취소가: {cell_data["cancel_buy_price"]}``', inline=False)

                    elif cell_data["status"] == "s2 waiting...":
                        embed.add_field(name=f"{cell_num}", value=f'``cell 자금: {cell_data["funds"]}  ||  cell 상태: 판매오더 체결 대기중...\n판매금액: {cell_data["sell_price"]}  ||  코인 갯수: {cell_data["buy_coin_num"]}\n판매오더 취소가: {cell_data["cancel_sell_price"]}``', inline=False)

                    else:
                        embed.add_field(name=f"{cell_num}", value=f'``cell 자금: {cell_data["funds"]}  ||  cell 상태: 구매 대기중...``', inline=False)
            mes1 = await self.client.get_channel(919929973324787782).fetch_message(config_data["status_message_id_1"])
            await mes1.edit(content = "",embed = embed)
            t.sleep(5)
            mes2 = await self.client.get_channel(949429988803891290).fetch_message(config_data["status_message_id_2"])
            await mes2.edit(content = "",embed = embed)
            
            
        except Exception as e:
            print(f'status system error: {e}')
            
    @status.before_loop
    async def before_status_loop(self):
        print('status System: waiting for bot on...')
        await self.client.wait_until_ready()
        print('status System Online!')


async def setup(client):
    await client.add_cog(status(client))