#%%
import pyupbit
import datetime as dt
import yaml
import time as t



config_loc = "C:/python/Auto_coin/Auto_coin_trading_v2.1.0/Auto_trading/config.yaml"
data_loc = "C:/python/Auto_coin/Auto_coin_trading_v2.0.1/Auto_trading/data.yaml"
bridge_loc = "C:/python/Auto_coin/Auto_coin_trading_v2.0.1/bridge"
loop_count = 0


with open(config_loc, encoding='utf-8') as f:
    config_data = yaml.load(f, Loader=yaml.FullLoader)
upbit = pyupbit.Upbit(config_data["access"],config_data["secret"])

print(config_data["coin_type"])


now_price = pyupbit.get_current_price(config_data["coin_type"])

coin_holdings = upbit.get_balance(config_data["coin_type"])
print(coin_holdings)

upbit.get_order(config_data["coin_type"])


# %%
