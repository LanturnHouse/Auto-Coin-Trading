#%%
import pyupbit
import yaml


config_loc = "./config.yaml"
data_loc = "./data.yaml"


with open(config_loc, encoding='utf-8') as f:
    config_data = yaml.load(f, Loader=yaml.FullLoader)
with open(data_loc, encoding='utf-8') as f:
    data_data = yaml.load(f, Loader=yaml.FullLoader)

    
upbit = pyupbit.Upbit(config_data["access"],config_data["secret"])

print(upbit.get_balances())
print("\n\n\n")
print(upbit.get_balance())
print(upbit.get_balances()[0])

print("\n")
for i in upbit.get_balances():
    if i['currency'] == "NEAR":
        print(i['avg_buy_price'])
    print(i)
# %%
