#%%
import pyupbit
import yaml



config_loc = "C:/Users/JuJin/Desktop/coin/Auto_trading/config.yaml"
data_loc = "C:/Users/JuJin/Desktop/coin/Auto_trading/data.yaml"
bridge_data_loc = "C:/Users/JuJin/Desktop/coin/bridge/status/"


with open(config_loc, encoding='utf-8') as f:
    config_data = yaml.load(f, Loader=yaml.FullLoader)
with open(data_loc, encoding='utf-8') as f:
    data_data = yaml.load(f, Loader=yaml.FullLoader)

    
upbit = pyupbit.Upbit(config_data["access"],config_data["secret"])
    
    
for i in range(0,4):
    with open(bridge_data_loc + f"cell {i}.yaml", encoding='utf-8') as f:
        bridge_data = yaml.load(f, Loader=yaml.FullLoader)
    bridge_data["status"] = "b waiting..."
    with open(bridge_data_loc + f"cell {i}.yaml", 'w', encoding = 'utf-8') as outfile:
        yaml.dump(bridge_data, outfile, indent = 4, allow_unicode = True)

with open(bridge_data_loc + "main_status.yaml", encoding='utf-8') as f:
    bridge_data = yaml.load(f, Loader=yaml.FullLoader)
now_revenue = upbit.get_balance("KRW")
yield_list = data_data["yield_list"]

yield_list[0] = now_revenue
bridge_data["yield_t1-1"] = round(now_revenue / yield_list[1] * 100 - 100, 3)
bridge_data["yield_t1-7"] = round(now_revenue / yield_list[7] * 100 - 100, 3)
bridge_data["yield_t1-30"] = round(now_revenue / yield_list[30] * 100 - 100, 3)
bridge_data["yield_t2-1"] = round(now_revenue - yield_list[1], 3)
bridge_data["yield_t2-7"] = round(now_revenue - yield_list[7], 3)
bridge_data["yield_t2-30"] = round(now_revenue - yield_list[30], 3)

data_data["buy_order"] = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
data_data["sell_order"] = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
data_data["coin_buy_list"] = [0,0,0,0,0]
data_data["coin_sell_list"] = [0,0,0,0,0]
data_data["coin_buy_num"] = [0,0,0,0,0]
data_data["sell_type"] = ['','','','','']
data_data["avg_value"] = 0.0

with open(bridge_data_loc + "status", 'w', encoding = 'utf-8') as outfile:
    yaml.dump(bridge_data, outfile, indent = 4, allow_unicode = True)
with open(data_loc, 'w', encoding = 'utf-8') as outfile:
    yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)







print(upbit.get_balance("KRW"))
now_price = pyupbit.get_current_price(config_data["coin_type"])

coin_holdings = upbit.get_balance(config_data["coin_type"])
print(coin_holdings)

upbit.sell_limit_order(config_data["coin_type"] ,now_price ,coin_holdings)
# %%
