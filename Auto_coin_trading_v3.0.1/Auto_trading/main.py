#%%
import pyupbit
import datetime as dt
import yaml
import time as t

import lib.check as ck
import lib.order_handler as oh
import lib.re_date as rd
import lib.pyupbit_convenience as pc



config_loc = "C:/Users/JuJin/Desktop/coin/Auto_trading/config.yaml"
data_loc = "C:/Users/JuJin/Desktop/coin/Auto_trading/data.yaml"
bridge_loc = "C:/Users/JuJin/Desktop/coin/bridge"
loop_count = 0


with open(config_loc, encoding='utf-8') as f:
    config_data = yaml.load(f, Loader=yaml.FullLoader)
upbit = pyupbit.Upbit(config_data["access"],config_data["secret"])



# rd.re_date_f(data_loc)



while True:
    
    
    with open(config_loc, encoding='utf-8') as f:
        config_data = yaml.load(f, Loader=yaml.FullLoader)
        
    with open(data_loc, encoding='utf-8') as f:
        data_data = yaml.load(f, Loader=yaml.FullLoader)
    
    df = pyupbit.get_ohlcv(config_data["coin_type"],interval = 'minute5' ,count = 4)
    df = df.reset_index()
    
    
    coin_buy_list = data_data['coin_buy_list']
    coin_sell_list = data_data['coin_sell_list']
    cell_funds = data_data['cell_funds']
    buy_order = data_data['buy_order']
    now_price = float(df.at[3,"open"])
    pc_ = pc.pyupbit_cal(10, config_data["coin_type"])
    limit = pc_.get_asking_price(now_price)
    tick_value = round(pc_.limit_check())
    

    print('────────────────────────────────────────────────────────────────')
    print(f"check start time: {dt.datetime.now()}")
    print(f'현재 KRW 잔액: {upbit.get_balance("KRW")}')
    print('┌───────────────────────────────────────')
    print(f"│  Buy Active: {config_data['active']}")
    print(f"│  Start price: {now_price}")
    print(f"│  호가 단위: {limit}")
    print(f"│  틱 단위: {tick_value}")
    
    
    
    
    
    rd.auto_dr(data_loc)
    
    order = oh.oh(upbit,df,limit)
    
    # 구매오더 및 판매오더 체결 확인
    order.check_buy_order(now_price)
    order.check_sell_order(now_price)
    
    
    
    while True:
        
        try:
            df_ = pyupbit.get_ohlcv(config_data["coin_type"],interval = 'minute5' ,count = 4)
            df_ = df_.reset_index()
        except Exception as e:
            print(e)
            continue
        if df_.at[2,'close'] != df.at[2,'close'] or df_.at[2,'open'] != df.at[2,'open'] or df_.at[2,'high'] != df.at[2,'high'] or df_.at[2,'low'] != df.at[2,'low']:
            break
        try:
            f = open(f"{bridge_loc}/program_active_check.txt", 'w')
            f.close()
            del f
        except Exception as e:
            print(f"active check program Error! {e}")
        t.sleep(5)


    df = pyupbit.get_ohlcv(config_data["coin_type"],interval = 'minute5' ,count = 4)
    df = df.reset_index()

    now_price = float(df.at[2,'close'])
    
    check = ck.ck(df, now_price, limit, upbit, tick_value)
    
    
    ccs = check.circulation_sell()
    if ccs != False:
        print(f'│  circulation check: {ccs}')
        order.circulation_sell_order(now_price, ccs)
    
    order.oh_dump()
    
    bc = check.buy_check()
    sc = check.sell_check()
    csc = check.cut_sell()
    
    order = oh.oh(upbit,df,limit)
    
    print(f'│  buy check: {bc}')
    print(f'│  sell check: {sc}')


    order.new_buy_order(now_price, bc)
    
    # 판매오더
    order.new_sell_order(now_price, sc)
    order.new_sell_order(now_price, csc)
    
    
    order.oh_dump()
    
    print(f"│  End price: {now_price}")
    
    del order
    del check
    
    
        
    print('└───────────────────────────────────────')
    print("loop done...")
    print(f"check end time: {dt.datetime.now()}")
    print('────────────────────────────────────────────────────────────────\n\n')


# %%
