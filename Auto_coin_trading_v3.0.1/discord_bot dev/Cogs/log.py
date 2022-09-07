import discord
import yaml
import os
import time as t
from discord.ext import commands, tasks

path = "C:/Users/JuJin/Desktop/coin/bridge"
config_loc = "C:/Users/JuJin/Desktop/coin/discord_bot/config.yaml"
with open(config_loc, encoding='utf-8') as f:
    config_data = yaml.load(f, Loader=yaml.FullLoader)
    
    
class log(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.send_log.start()

    @tasks.loop(seconds = 1)
    async def send_log(self):
        try:
            file_list = os.listdir(path)
            for file_name in file_list:
                if file_name.startswith('registration_buy_order'):
                    # 구매오더 등록
                    print('구매오더 등록')
                    with open(f"{path}/{file_name}" , encoding= 'utf-8') as f:
                        new_buy_order_data = yaml.load(f, Loader=yaml.FullLoader)
                    with open(f'{path}/status/cell {new_buy_order_data[0]["cell"]}.yaml' , encoding= 'utf-8') as f:
                        cell_data = yaml.load(f, Loader=yaml.FullLoader)
                    new_buy_order_data = new_buy_order_data[0]
                    cell_data["status"] = new_buy_order_data["cell_status"]
                    cell_data["buy_price"] = new_buy_order_data["buy_price"]
                    cell_data["buy_coin_num"] = new_buy_order_data["buy_coin_num"]
                    cell_data["cancel_buy_price"] = new_buy_order_data['cancel_buy_price']
                    t.sleep(1)
                    os.remove(f"{path}/{file_name}")

                    embed=discord.Embed(title="거래 log", color=0x32CD32)
                    embed.add_field(name=f"order type", value=f"``구매오더 등록 | cell {new_buy_order_data['cell']}``", inline=False)
                    embed.add_field(name=f"order uuid", value=f"``{new_buy_order_data['buy_order']['uuid']}``", inline=False)
                    embed.add_field(name=f"코인 갯수", value=f"``{new_buy_order_data['buy_coin_num']}``", inline=False)
                    embed.add_field(name=f"구매가격", value=f"``{new_buy_order_data['buy_price']}``", inline=False)
                    embed.add_field(name=f"구매오더 취소가", value=f"``{new_buy_order_data['cancel_buy_price']}``", inline=False)
                    with open(f'{path}/status/cell {new_buy_order_data["cell"]}.yaml', 'w', encoding = 'utf-8') as outfile:
                        yaml.dump(cell_data, outfile, indent = 4, allow_unicode = True)
                    await self.client.get_channel(config_data["log_channel"]).send(embed = embed)
                    await self.client.get_channel(925085422600716348).send(embed = embed)




                if file_name.startswith('registration_sell_order'):
                    # 판매오더 등록
                    print('판매오더 등록')
                    with open(f"{path}/{file_name}" , encoding= 'utf-8') as f:
                        new_sell_order_data = yaml.load(f, Loader=yaml.FullLoader)
                    t.sleep(1)
                    os.remove(f"{path}/{file_name}")

                    for i in new_sell_order_data:
                        with open(f'{path}/status/cell {new_sell_order_data[i]["cell"]}.yaml' , encoding= 'utf-8') as f:
                            cell_data = yaml.load(f, Loader=yaml.FullLoader)
                        cell_data["status"] = new_sell_order_data[i]["cell_status"]
                        cell_data["sell_price"] = new_sell_order_data[i]["sell_price"]
                        cell_data["cancel_sell_price"] = new_sell_order_data[i]["cancel_sell_price"]
                        
                        embed=discord.Embed(title="거래 log", description = f"판매 Type: {new_sell_order_data[i]['sell_type']}", color=0xBA55D3)
                        embed.add_field(name=f"order type", value=f"``판매오더 등록 | cell {new_sell_order_data[i]['cell']}``", inline=False)
                        embed.add_field(name=f"order uuid", value=f"``{new_sell_order_data[i]['sell_order']['uuid']}``", inline=False)
                        embed.add_field(name=f"코인 갯수", value=f"``{new_sell_order_data[i]['sell_coin_num']}``", inline=False)
                        embed.add_field(name=f"판매가격", value=f"``{new_sell_order_data[i]['sell_price']}``", inline=False)
                        embed.add_field(name=f"판매오더 취소가", value=f"``{new_sell_order_data[i]['cancel_sell_price']}``", inline=False)
                        with open(f'{path}/status/cell {new_sell_order_data[i]["cell"]}.yaml', 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(cell_data, outfile, indent = 4, allow_unicode = True)
                        await self.client.get_channel(config_data["log_channel"]).send(embed = embed)
                        await self.client.get_channel(925085501596250173).send(embed = embed)

                

                if file_name.startswith('cut_sell_order'):
                    # 손절
                    print('손절 판매')

                    with open(f"{path}/{file_name}" , encoding= 'utf-8') as f:
                        new_cut_sell_data = yaml.load(f, Loader=yaml.FullLoader)
                    t.sleep(1)
                    os.remove(f"{path}/{file_name}")

                    for i in new_cut_sell_data:
                        with open(f'{path}/status/cell {new_cut_sell_data[i]["cell"]}.yaml' , encoding= 'utf-8') as f:
                            cell_data = yaml.load(f, Loader=yaml.FullLoader)
                        cell_data["status"] = new_cut_sell_data[i]["cell_status"]
                        cell_data["sell_price"] = 0.0
                        cell_data["cut_sell_price"] = 0.0
                        cell_data["funds"] = round(new_cut_sell_data[i]["cell_funds"])
                        embed=discord.Embed(title="거래 log", color=0xFF4500)
                        embed.add_field(name=f"order type", value=f"``손절판매 | {new_cut_sell_data[i]['sell_bool']}``", inline=False)
                        embed.add_field(name=f"코인 갯수", value=f"``{new_cut_sell_data[i]['buy_coin_num']}``", inline=False)
                        embed.add_field(name=f"판매가격", value=f"``{new_cut_sell_data[i]['sell_price']}``", inline=False)
                        embed.add_field(name=f"수익률", value=f"``{new_cut_sell_data[i]['ror']}``", inline=False)
                        embed.add_field(name=f"cell 자금", value=f"``{new_cut_sell_data[i]['cell_funds']}``", inline=False)
                        with open(f'{path}/status/cell {new_cut_sell_data[i]["cell"]}.yaml', 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(cell_data, outfile, indent = 4, allow_unicode = True)
                        await self.client.get_channel(config_data["log_channel"]).send(embed = embed)
                        await self.client.get_channel(925085546081054730).send(embed = embed)


                if file_name.startswith('tightening_sell_order'):
                    # 판매오더 체결
                    print('판매오더 체결')

                    with open(f"{path}/{file_name}" , encoding= 'utf-8') as f:
                        data_data = yaml.load(f, Loader=yaml.FullLoader)
                    t.sleep(1)
                    os.remove(f"{path}/{file_name}")

                    for i in data_data:
                        with open(f'{path}/status/cell {data_data[i]["cell"]}.yaml' , encoding= 'utf-8') as f:
                            cell_data = yaml.load(f, Loader=yaml.FullLoader)
                        cell_data["status"] = data_data[i]["cell_status"]
                        cell_data["sell_price"] = 0.0
                        cell_data["cut_sell_price"] = 0.0
                        cell_data["funds"] = round(data_data[i]["cell_funds"])
                        embed=discord.Embed(title="거래 log", color=0xFFFFFF)
                        embed.add_field(name=f"order type", value=f"``판매오더 체결 | cell {data_data[i]['cell']}``", inline=False)
                        embed.add_field(name=f"코인 갯수", value=f"``{data_data[i]['sell_coin_num']}``", inline=False)
                        embed.add_field(name=f"판매가격", value=f"``{data_data[i]['sell_price']}``", inline=False)
                        embed.add_field(name=f"수익률", value=f"``{data_data[i]['ror']}``", inline=False)
                        embed.add_field(name=f"cell 자금", value=f"``{data_data[i]['cell_funds']}``", inline=False)

                        with open(f'{path}/status/cell {data_data[i]["cell"]}.yaml', 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(cell_data, outfile, indent = 4, allow_unicode = True)
                        await self.client.get_channel(config_data["log_channel"]).send(embed = embed)
                        await self.client.get_channel(925085521993138206).send(embed = embed)
                        
                        if data_data[i]["sell_type"] == "nomal":
                            with open(f'{path}/status/main_status.yaml' , encoding= 'utf-8') as f:
                                    status_data = yaml.load(f, Loader=yaml.FullLoader)
                            status_data["yield_t1-1"] = data_data[i]["yield_t1-1"]
                            status_data["yield_t1-7"] = data_data[i]["yield_t1-7"]
                            status_data["yield_t1-30"] = data_data[i]["yield_t1-30"]
                            status_data["yield_t2-1"] = data_data[i]["yield_t2-1"]
                            status_data["yield_t2-7"] = data_data[i]["yield_t2-7"]
                            status_data["yield_t2-30"] = data_data[i]["yield_t2-30"]
                            
                            with open(f'{path}/status/main_status.yaml', 'w', encoding = 'utf-8') as outfile:
                                yaml.dump(status_data, outfile, indent = 4, allow_unicode = True)

                if file_name.startswith('cancellation_sell_order'):
                    # 판매오더 취소
                    print('판매오더 취소')

                    with open(f"{path}/{file_name}" , encoding= 'utf-8') as f:
                        data_data = yaml.load(f, Loader=yaml.FullLoader)
                    t.sleep(1)
                    os.remove(f"{path}/{file_name}")

                    for i in data_data:
                        with open(f'{path}/status/cell {data_data[i]["cell"]}.yaml' , encoding= 'utf-8') as f:
                            cell_data = yaml.load(f, Loader=yaml.FullLoader)
                        cell_data["status"] = data_data[i]["cell_status"]
                        cell_data["sell_price"] = 0.0
                        cell_data["cut_sell_price"] = 0.0
                        embed=discord.Embed(title="거래 log", color=0xFFFF00)
                        embed.add_field(name=f"order type", value=f"``판매오더 취소 | cell {data_data[i]['cell']}``", inline=False)
                        embed.add_field(name=f"코인 갯수", value=f"``{data_data[i]['sell_coin_num']}``", inline=False)
                        embed.add_field(name=f"판매가격", value=f"``{data_data[i]['sell_price']}``", inline=False)

                        with open(f'{path}/status/cell {data_data[i]["cell"]}.yaml', 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(cell_data, outfile, indent = 4, allow_unicode = True)
                        await self.client.get_channel(config_data["log_channel"]).send(embed = embed)
                        await self.client.get_channel(925085501596250173).send(embed = embed)

                if file_name.startswith('tightening_buy_order'):
                    # 구매오더 체결
                    print('구매오더 체결')

                    with open(f"{path}/{file_name}" , encoding= 'utf-8') as f:
                        data_data = yaml.load(f, Loader=yaml.FullLoader)
                    t.sleep(1)
                    os.remove(f"{path}/{file_name}")

                    for i in data_data:
                        with open(f'{path}/status/cell {data_data[i]["cell"]}.yaml' , encoding= 'utf-8') as f:
                            cell_data = yaml.load(f, Loader=yaml.FullLoader)
                        cell_data["status"] = data_data[i]["cell_status"]
                        cell_data["sell_price"] = data_data[i]['target_coin_sell_price']
                        embed=discord.Embed(title="거래 log", color=0xFFFF00)
                        embed.add_field(name=f"order type", value=f"``구매오더 체결 | cell {data_data[i]['cell']}``", inline=False)
                        embed.add_field(name=f"코인 갯수", value=f"``{data_data[i]['buy_coin_num']}``", inline=False)
                        embed.add_field(name=f"코인 판매가격", value=f"``{data_data[i]['target_coin_sell_price']}``", inline=False)

                        with open(f'{path}/status/cell {data_data[i]["cell"]}.yaml', 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(cell_data, outfile, indent = 4, allow_unicode = True)
                        await self.client.get_channel(config_data["log_channel"]).send(embed = embed)
                        await self.client.get_channel(925085461976850492).send(embed = embed)


                if file_name.startswith('cancellation_buy_order'):
                    # 구매오더 취소
                    print(7)

                    with open(f"{path}/{file_name}" , encoding= 'utf-8') as f:
                        data_data = yaml.load(f, Loader=yaml.FullLoader)
                    t.sleep(1)
                    os.remove(f"{path}/{file_name}")

                    for i in data_data:
                        with open(f'{path}/status/cell {data_data[i]["cell"]}.yaml' , encoding= 'utf-8') as f:
                            cell_data = yaml.load(f, Loader=yaml.FullLoader)
                        cell_data["status"] = data_data[i]["cell_status"]
                        cell_data["sell_price"] = 0.0
                        cell_data["cut_sell_price"] = 0.0
                        embed=discord.Embed(title="거래 log", color=0xFFFF00)
                        embed.add_field(name=f"order type", value=f"``구매오더 취소 | cell {data_data[i]['cell']}``", inline=False)
                        embed.add_field(name=f"코인 갯수", value=f"``{data_data[i]['sell_coin_num']}``", inline=False)

                        with open(f'{path}/status/cell {data_data[i]["cell"]}.yaml', 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(cell_data, outfile, indent = 4, allow_unicode = True)
                        await self.client.get_channel(config_data["log_channel"]).send(embed = embed)
                        await self.client.get_channel(925085422600716348).send(embed = embed)




        except Exception as e:
            print(f"log system error: {e}")

    @send_log.before_loop
    async def before_send_log(self):
        print('log System: waiting for bot on...')
        await self.client.wait_until_ready()
        print("log System Online")



async def setup(client):
    await client.add_cog(log(client))
