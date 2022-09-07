import pyupbit
import yaml
import time as t
import datetime as dt
from discord.ext import commands

config_loc = "C:/Users/JuJin/Desktop/coin/discord_bot/config.yaml"
a_config_loc = "C:/Users/JuJin/Desktop/coin/Auto_trading/config.yaml"
a_data_loc = "C:/Users/JuJin/Desktop/coin/Auto_trading/data.yaml"
channel_list = [925085422600716348, 925085461976850492, 925085501596250173, 925085521993138206, 925085546081054730]



def list_zero_check(alist):
    count = 0
    for i in alist:
        if i != 0.0:
            count = count + 1
    return count

#========================== log
bridge_loc = "C:/Users/JuJin/Desktop/coin/bridge"

class set_log:
    
    def __init__(self,file_name):
        self.log = {}
        self.count = 0
        self.file_name = file_name
    

    def add_log(self,l_dic: dict):
        self.log[self.count] = l_dic
        self.count += 1
        del l_dic
    
    def dump_log(self):
        if self.log != {}:
            f = open(f"{bridge_loc}/{self.file_name}.yaml", 'w')
            yaml.dump(self.log, f, indent = 4, allow_unicode = True)
            f.close()
            del f
#========================== log



#================
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
#================






class c_command(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name = "set_status_message_1")
    async def send_command_message(self,ctx):
        with open(config_loc, encoding='utf-8') as f:
            config_data = yaml.load(f, Loader=yaml.FullLoader)
        mes = await ctx.send("이 메세지가 status message 1로 지정되었습니다.")
        config_data["status_message_id_1"] = mes.id
        with open(config_loc, 'w', encoding = 'utf-8') as outfile:
            yaml.dump(config_data, outfile, indent = 4, allow_unicode = True)

    @commands.command(name = "set_status_message_2")
    async def send_command_message(self,ctx):
        with open(config_loc, encoding='utf-8') as f:
            config_data = yaml.load(f, Loader=yaml.FullLoader)
        mes = await ctx.send("이 메세지가 status message 2로 지정되었습니다.")
        config_data["status_message_id_2"] = mes.id
        with open(config_loc, 'w', encoding = 'utf-8') as outfile:
            yaml.dump(config_data, outfile, indent = 4, allow_unicode = True)
    


    @commands.command(name = "cut_log")
    async def cut_log(self, ctx):
        print('log cut')

        for cl in channel_list:
            print(f'cut log channel id: {cl}')
            await self.client.get_channel(int(cl)).send(f'.\n\n\n\n\n시작 시간: {dt.datetime.now()}')


    @commands.command(name = "판매")
    async def sell_cell(self, ctx, cell_num):
        with open(a_config_loc, encoding='utf-8') as f:
            a_config_data = yaml.load(f, Loader=yaml.FullLoader)
        with open(a_data_loc, encoding='utf-8') as f:
            a_data_data = yaml.load(f, Loader=yaml.FullLoader)
            
        upbit = pyupbit.Upbit(a_config_data["access"],a_config_data["secret"])
        rso = set_log("registration_sell_order")
        now_price = pyupbit.get_current_price(a_config_data["coin_type"])
        if a_data_data.coin_sell_list[cell_num] != 0.0:
            if a_data_data.buy_order[cell_num]["state"] == "done":
                print(f"│  판매 조건 만족.")
                if list_zero_check(a_data_data.coin_sell_list) == 1:
                    coin_holdings = upbit.get_balance(a_config_data["coin_type"])
                    s_order = upbit.sell_limit_order(a_config_data["coin_type"] ,now_price ,coin_holdings)
                    a_data_data.coin_buy_num[cell_num] = coin_holdings
                else:
                    s_order = upbit.sell_limit_order(a_config_data["coin_type"] ,now_price ,float(a_data_data.coin_buy_num[cell_num]))
                    
                print(f"│  cell {cell_num} selling...")
                print(f"│  cell {cell_num} 보유 코인: {a_data_data.buy_order[cell_num]['volume']}")
                a_data_data.sell_order[cell_num] = s_order
                print(f'│  sell order uuid: {s_order["uuid"]}')
                print(f'│  coin sell num: {s_order["volume"]}')
                
                rso.add_log({"sell_order": s_order,
                            "sell_coin_num": a_data_data.coin_buy_num[cell_num],
                            "sell_price": now_price,
                            "cancel_sell_price": now_price - get_asking_price(now_price) * 2,
                            "cell": cell_num,
                            "cell_status": "s2 waiting...",
                            "sell_type": "nomal"})
                print(f"│  판매오더 등록 완료!")
                a_data_data.sell_type[cell_num] = 'nomal'
                t.sleep(0.3)
                rso.dump_log()
            else:
                await ctx.send(f"cell {cell_num}의 구매오더가 아직 체결되지 않았습니다.")
        else:
            await ctx.send(f"cell {cell_num}에는 판매할 코인이 없습니다.")





    @commands.command(name = "구매")
    async def cell_buy(self,ctx,cell_num):
        
        with open(a_config_loc, encoding='utf-8') as f:
            a_config_data = yaml.load(f, Loader=yaml.FullLoader)
        with open(a_data_loc, encoding='utf-8') as f:
            a_data_data = yaml.load(f, Loader=yaml.FullLoader)
            
        upbit = pyupbit.Upbit(a_config_data["access"],a_config_data["secret"])
        now_price = pyupbit.get_current_price(a_config_data["coin_type"])
        rbo = set_log("registration_buy_order")
        if a_data_data.coin_buy_list[cell_num] == 0.0:
            print(f"│  구매 조건 만족.")
            print(f"│  cell {cell_num}: coin Buying...")
            print(f'│  cell funds: {a_data_data.cell_funds[cell_num]}')
            a_data_data.coin_buy_num[cell_num] = a_data_data.cell_funds[cell_num] / float(now_price)
            b_order = upbit.buy_limit_order(a_data_data.config_data["coin_type"], now_price, a_data_data.coin_buy_num[cell_num])
            a_data_data.buy_order[cell_num] = b_order
            
            print(f"│  coin buy num: {a_data_data.coin_buy_num[cell_num]}")
            print(f'│  buy order uuid: {b_order["uuid"]}')
            
            a_data_data.coin_sell_list[cell_num] = now_price + get_asking_price(now_price) * 2
            
            a_data_data.coin_buy_list[cell_num] = float(b_order["price"])
            rbo.add_log({"buy_order": b_order,
                        "buy_coin_num": a_data_data.coin_buy_num[cell_num],
                        "buy_price": now_price,
                        "cell": cell_num,
                        "cell_status": "b2 waiting...",
                        "cancel_buy_price": now_price + get_asking_price(now_price) * 2})
            print("│  구매오더 등록 완료")
            rbo.dump_log()
        else:
            await ctx.send(f"cell {cell_num}은 이미 코인이 구매되어 있습니다.")


async def setup(client):
    await client.add_cog(c_command(client))