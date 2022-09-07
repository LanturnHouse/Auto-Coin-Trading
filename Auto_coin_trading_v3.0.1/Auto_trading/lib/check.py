import yaml
import pyupbit

data_loc = "C:/Users/JuJin/Desktop/coin/Auto_trading/data.yaml"
config_loc = "C:/Users/JuJin/Desktop/coin/Auto_trading/config.yaml"





def mid_value(open_p, end_p):
    if open_p + end_p == 0:
        return end_p
    else:
        return (open_p + end_p) / 2





class ck:
    
    def __init__(self, df, now_price, limit,upbit, tick_value):
        with open(data_loc, encoding='utf-8') as f:
            data_data = yaml.load(f, Loader=yaml.FullLoader)
        self.df = df
        self.limit = limit
        self.now_price = now_price
        self.upbit = upbit
        self.tick_value = tick_value
        if data_data["coin_buy_list"][4] != 0:
            data_data['circulation'] = True
        with open(data_loc, 'w', encoding = 'utf-8') as outfile:
            yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
        print(f"│  순환매: {data_data['circulation']}")
            
            
            
        
        

    def buy_check(self):
        with open(data_loc, encoding='utf-8') as f:
            data_data = yaml.load(f, Loader=yaml.FullLoader)
            
            
        print(f"│  buy checking...")
        if data_data["tick_stack"] == 6:
            data_data["tick_stack"] = 0
            data_data['tick'] = 0
            data_data['tick_end_price'] = 0
            print('│  tick stack over')
            with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
            return False
        
        if data_data['tick'] == 0:
            data_data["tick_stack"] += 1
            with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
            if self.df.at[2, 'close'] - self.df.at[2, 'low'] >= self.limit * 1:
                if self.df.at[2, "open"] - self.df.at[2, "close"] >= self.tick_value:
                    if data_data["coin_buy_list"][0] != 0:
                        if float(self.df.at[2, "close"]) <= float(data_data["avg_value"]):
                            print('│  tick start 1')
                            data_data['tick'] += 1
                            data_data['tick_end_price'] = int(self.df.at[2,'close'])
                            print(f'│  tick: {data_data["tick"]}')
                            with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                                yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
                            return False
                        
                    else:
                        print('│  tick start 2')
                        data_data['tick'] += 1
                        data_data['tick_end_price'] = int(self.df.at[2,'close'])
                        print(f'│  tick: {data_data["tick"]}')
                        with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
                        return False
        else:
            if data_data['tick'] == 1:
                if mid_value(self.df.at[1,'open'], self.df.at[1,'close']) - mid_value(self.df.at[2,'open'], self.df.at[2,'close']) < self.tick_value:
                    data_data['tick'] = 0
                    data_data['tick_end_price'] = 0
                    print('│  tick reset t1')
                    with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                        yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
                    return False
                    
                elif self.df.at[2,'close'] - data_data['tick_end_price'] >= self.limit * 4:
                    data_data['tick'] = 0
                    data_data['tick_end_price'] = 0
                    print('│  tick reset t2')
                    with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                        yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
                    return False
            """
            if data_data["coin_buy_list"][0] != 0:
                
                if self.df.at[2, 'close'] - self.df.at[2, 'low'] >= self.limit * 1:
                    if (data_data['tick_end_price'] - self.df.at[2,'close'] >= self.tick_value and
                        ((self.df.at[1,'open'] > self.df.at[1,'close'] and self.df.at[2,'open'] > self.df.at[2,'close']) or
                        (self.df.at[2,'open'] - self.df.at[2,'close'] >= self.tick_value))):
                        
                        data_data['tick_end_price'] = float(self.df.at[2,'close'])
                        data_data['tick'] += 1
                        print('│  tick + 1')
                        print(f'│  tick: {data_data["tick"]}')
                        with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
                        if data_data['tick'] >= 3:
                            return True
                        else:
                            return  False
                        
                    else:
                        print('│  tick continue')
                        print(f'│  tick: {data_data["tick"]}')
                        with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                                yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
                                return False
                else:
                    print('│  tick continue')
                    print(f'│  tick: {data_data["tick"]}')
                    with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
                            return False
                
            else:
            """
            
            if self.df.at[2,'close'] - data_data['tick_end_price'] >= self.limit * 4 or (self.df.at[1,'open'] < self.df.at[1,'close'] and self.df.at[2,'open'] < self.df.at[2,'close'] and self.df.at[2,'close'] - self.df.at[1,'close'] > self.tick_value * 2) or (self.df.at[1, "open"] > self.df.at[1, "close"] and self.df.at[1, "open"] < self.df.at[2, "close"]):
                data_data['tick'] = 0
                data_data['tick_end_price'] = 0
                print('│  tick 초기화')
                print(f'│  tick: {data_data["tick"]}')
                with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                    yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
                return False

            if self.df.at[2, 'close'] - self.df.at[2, 'low'] >= self.limit * 1:
                print(1111)
                if data_data['tick_end_price'] - self.df.at[2,'close'] >= self.tick_value:
                    print(2222)
                    data_data['tick'] += 1
                    data_data['tick_end_price'] = int(self.df.at[2,'close'])
                    print('│  tick + 1')
                    print(f'│  tick: {data_data["tick"]}')
                    with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                        yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
                    if data_data['tick'] >= 3:
                        return True
            
            else:
                print('│  tick continue')
                print(f'│  tick: {data_data["tick"]}')
                return False
            
        return False
        
    
    
    
    
    
    
    
    
    def sell_check(self):
        with open(data_loc, encoding='utf-8') as f:
            data_data = yaml.load(f, Loader=yaml.FullLoader)
        with open(config_loc, encoding='utf-8') as f:
            config_data = yaml.load(f, Loader=yaml.FullLoader)
        
        print(f"│  sell checking...")
        
        # 이 부분 data.yaml안의 자료로 비교를 하는게 아닌 uuid를 기반으로 state를 리퀘스트해서 받아오도록 바꿔야함.
        for b_order_index_num in data_data['buy_order']:
            if data_data['buy_order'][b_order_index_num] != 0:
                if data_data['buy_order'][b_order_index_num]['state'] != 'done':
                    return False

        
        b_cell_funds = 0.0
        a_cell_funds = 0.0
        for a in range(0,5):
            if data_data["buy_order"][a] == 0:
                a_cell_funds += float(data_data["cell_funds"][a])
                b_cell_funds += float(data_data["cell_funds"][a])
            else:
                a_cell_funds += float(data_data["coin_buy_num"][a]) * float(self.now_price)
                b_cell_funds += float(data_data["coin_buy_num"][a]) * float(data_data["coin_buy_list"][a])
                
        print(f'│  before: {b_cell_funds}')
        print(f'│  after: {a_cell_funds}')
    
        if sum(data_data['coin_buy_list']) != 0:
            # if self.now_price >= float(data_data['avg_value']):
            if self.now_price - float(data_data["avg_value"]) >= self.limit * 2:
                
                    
                
                Yield = ((a_cell_funds + ((self.now_price - float(data_data["avg_value"])) * self.upbit.get_balance(config_data["coin_type"]))) / (a_cell_funds) * 100) - 100
                print(f'│  수익률: {Yield}')
                
                
                if float(a_cell_funds) >= float(b_cell_funds):

                    # if (self.df.at[1,'open'] > self.df.at[1,'close']) and self.df.at[1,'open'] - self.df.at[3, 'close'] >= self.tick_value:
                    if mid_value(self.df.at[0, 'open'], self.df.at[0, 'close']) < mid_value(self.df.at[1, 'open'], self.df.at[1, 'close']) < mid_value(self.df.at[2, 'open'], self.df.at[2, 'close']):
                        data_data['circulation'] = False
                        data_data['tick'] = 0
                        data_data['tick_end_price'] = 0
                        print("│  수익 판매")
                        with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
                        return True
                
                else:
                    print("│  본전 미도달. 판매 cancle")

        return False
            
       
    def circulation_sell(self):
        with open(data_loc, encoding='utf-8') as f:
            data_data = yaml.load(f, Loader=yaml.FullLoader)
        # 순환 판매
        if data_data['circulation'] == True:
            if data_data['coin_buy_list'][0] != 0:
                for e in range(4,3,-1):
                    if data_data['coin_buy_list'][e] != 0:
                        if data_data["coin_buy_list"][e] <= self.df.at[2, "close"]:
                            if mid_value(self.df.at[0,'open'], self.df.at[0,'close']) < mid_value(self.df.at[1,'open'], self.df.at[1,'close']) < mid_value(self.df.at[2,'open'], self.df.at[3, 'close']):
                                print('│  c sell')
                                data_data['sell_type'][e] = 'circulation'
                                
                                with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                                    yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
                                return e
        return False
    
    
    
    def cut_sell(self):
        with open(config_loc, encoding='utf-8') as f:
            config_data = yaml.load(f, Loader=yaml.FullLoader)
        df = pyupbit.get_ohlcv(config_data["coin_type"],interval = 'minute5' ,count = 6)
        df = df.reset_index()
        with open(data_loc, encoding='utf-8') as f:
            data_data = yaml.load(f, Loader=yaml.FullLoader)
        if data_data["coin_buy_list"][4] != 0:
            if df.at[0,"close"] <= df.at[1,"close"] <= df.at[2,"close"] >  df.at[3, "close"] > df.at[4, "close"] > df.at[5, "close"]:
                if df.at[3, "close"] - df.at[5, "close"] > self.tick_value:
                    if data_data["cut_sell"] == False:
                        print("│  손절 활성화")
                        data_data["cut_sell"] = True
                        with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
                    else:
                        data_data['circulation'] = False
                        data_data['tick'] = 0
                        data_data['tick_end_price'] = 0
                        print("│  손절 판매")
                        with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
                        return True
        