import yaml
import time as t
import os
from discord.ext import commands, tasks


a_data_loc = "C:/Users/JuJin/Desktop/coin/Auto_trading/data.yaml"



def check_dr():
    if os.path.isfile(f"C:/Users/JuJin/Desktop/coin/bridge/re date.txt"):
        os.remove(f"C:/Users/JuJin/Desktop/coin/bridge/re date.txt")
        return True



class daily_payment(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.daily_payment_.start()


    @tasks.loop(seconds = 10)
    async def daily_payment_(self):
        if check_dr():
            with open(a_data_loc, encoding='utf-8') as f:
                a_data_data = yaml.load(f, Loader=yaml.FullLoader)
        
        
            mes = f'''```ansi
[1;37m{t.strftime('%Y-%m-%d', t.localtime(t.time()))}[0m

[1;30m▨[0m KRW 보유 금액 (시작): [1;36m{a_data_data["yield_list"][1]}[0m
[1;30m▨[0m KRW 보유 금액 (마감): [1;36m{a_data_data["yield_list"][0]}[0m

[1;30m▨[0m 수익: [1;36m{a_data_data["yield_list"][0] - a_data_data["yield_list"][1]}[0m
[1;30m▨[0m 수익률: [1;36m{a_data_data["yield_list"][0] / a_data_data["yield_list"][1] * 100 - 100}[0m

[1;31m▨[0m 구매: [1;36m{a_data_data["buy_count"]}[0m
[1;34m▨[0m 판매: [1;36m{a_data_data["sell_count"]}[0m

```'''
            
            await self.client.get_channel(938963779067199518).send(mes)
        
    
    
    @daily_payment_.before_loop
    async def before_daily_payment__loop(self):
        print('daily payment System: waiting for bot on...')
        await self.client.wait_until_ready()
        print('daily payment System Online!')


async def setup(client):
    await client.add_cog(daily_payment(client))