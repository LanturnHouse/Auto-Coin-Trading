import yaml
import time as t

import lib.log as log
import lib.calculate as cal



data_loc = "C:/Users/JuJin/Desktop/coin/Auto_trading/data.yaml"
config_loc = "C:/Users/JuJin/Desktop/coin/Auto_trading/config.yaml"





class oh:
    
    def __init__(self,upbit,df,limit):
        with open(data_loc, encoding='utf-8') as f:
            data_data = yaml.load(f, Loader=yaml.FullLoader)
        with open(config_loc, encoding='utf-8') as f:
            config_data = yaml.load(f, Loader=yaml.FullLoader)
            
        self.data_data = data_data
        self.config_data = config_data
            
        self.limit = limit
        self.upbit = upbit
        
        self.df = df
        self.active = config_data['active']
        self.coin_buy_list = data_data['coin_buy_list']
        self.coin_sell_list = data_data['coin_sell_list']
        self.coin_buy_num = data_data['coin_buy_num']
        self.cell_funds = data_data['cell_funds']
        self.buy_order = data_data["buy_order"]
        self.sell_order = data_data["sell_order"]
        self.sell_type = data_data["sell_type"]
        self.yield_list = data_data["yield_list"]
        self.avg_value = data_data["avg_value"]
        self.b_date = self.data_data["b_date"]
        self.sell_half = self.data_data["sell_half"]
        self.sell_count = self.data_data["sell_count"]
        self.buy_count = data_data["buy_count"]
        
        
        
        
        
            



    
    def new_buy_order(self, now_price, bool):
        
        if bool == True:
            # 구매
            if self.active == True:
                
                
                rbo = log.set_log("registration_buy_order")
                for d in range(0,5):
                    if self.coin_buy_list[d] == 0.0:
                        print(f"│  구매 조건 만족.")
                        print(f"│  cell {d}: coin Buying...")
                        print(f'│  cell funds: {self.cell_funds[d]}')
                        self.coin_buy_num[d] = self.cell_funds[d] / float(now_price)
                        b_order = self.upbit.buy_limit_order(self.config_data["coin_type"], now_price, self.coin_buy_num[d])
                        self.buy_order[d] = b_order
                        
                        print(f"│  coin buy num: {self.coin_buy_num[d]}")
                        print(f'│  buy order uuid: {b_order["uuid"]}')
                        
                        self.coin_sell_list[d] = now_price + self.limit * 2
                        
                        self.coin_buy_list[d] = float(b_order["price"])
                        rbo.add_log({"buy_order": b_order,
                                    "buy_coin_num": self.coin_buy_num[d],
                                    "buy_price": now_price,
                                    "cell": d,
                                    "cell_status": "b2 waiting...",
                                    "cancel_buy_price": now_price + self.limit * 2})
                        print("│  구매오더 등록 완료")
                        break
                rbo.dump_log()
                    
                    
    def circulation_sell_order(self, now_price, cell_num):
        rso = log.set_log("registration_sell_order")
        if self.sell_order[cell_num] == 0:
            if self.coin_sell_list[cell_num] != 0.0:
                if self.buy_order[cell_num]["state"] == "done":
                    print(f"│  순환 판매 조건 만족.")
                    if cal.list_zero_check(self.coin_sell_list) == 1:
                        coin_holdings = self.upbit.get_balance(self.config_data["coin_type"])
                        s_order = self.upbit.sell_limit_order(self.config_data["coin_type"] ,now_price ,coin_holdings)
                        self.coin_buy_num[cell_num] = coin_holdings
                    else:
                        s_order = self.upbit.sell_limit_order(self.config_data["coin_type"] ,now_price ,self.buy_order[cell_num]["volume"])
                        
                    print(f"│  cell {cell_num} selling...")
                    print(f"│  cell {cell_num} 보유 코인: {self.buy_order[cell_num]['volume']}")
                    self.sell_order[cell_num] = s_order
                    print(f'│  sell order uuid: {s_order["uuid"]}')
                    print(f'│  coin sell num: {s_order["volume"]}')
                    
                    rso.add_log({"sell_order": s_order,
                                "sell_coin_num": self.coin_buy_num[cell_num],
                                "sell_price": now_price,
                                "cancel_sell_price": now_price - self.limit * 2,
                                "cell": cell_num,
                                "cell_status": "s2 waiting...",
                                "sell_type": 'circulation'})
                    print(f"│  판매오더 등록 완료!")
                    self.sell_type[cell_num] = 'circulation'
                
        rso.dump_log()
                

    def new_sell_order(self, now_price, type):
        
        # 판매
        print(f'│  현재 보유 코인 갯수:{self.upbit.get_balance(self.config_data["coin_type"])}')
        rso = log.set_log("registration_sell_order")
        if type == True:
            for k in range(0,5):
                if self.sell_order[k] == 0:
                    if self.coin_sell_list[k] != 0.0:
                        if self.buy_order[k]["state"] == "done":
                            print(f"│  판매 조건 만족.")
                            if cal.list_zero_check(self.coin_sell_list) == 1:
                                coin_holdings = self.upbit.get_balance(self.config_data["coin_type"])
                                s_order = self.upbit.sell_limit_order(self.config_data["coin_type"] ,now_price ,coin_holdings)
                                self.coin_buy_num[k] = coin_holdings
                            else:
                                s_order = self.upbit.sell_limit_order(self.config_data["coin_type"] ,now_price ,float(self.coin_buy_num[k]))
                                
                            print(f"│  cell {k} selling...")
                            print(f"│  cell {k} 보유 코인: {self.buy_order[k]['volume']}")
                            self.sell_order[k] = s_order
                            print(f'│  sell order uuid: {s_order["uuid"]}')
                            print(f'│  coin sell num: {s_order["volume"]}')
                            
                            rso.add_log({"sell_order": s_order,
                                        "sell_coin_num": self.coin_buy_num[k],
                                        "sell_price": now_price,
                                        "cancel_sell_price": now_price - self.limit * 2,
                                        "cell": k,
                                        "cell_status": "s2 waiting...",
                                        "sell_type": "nomal"})
                            print(f"│  판매오더 등록 완료!")
                            self.sell_type[k] = 'nomal'
                            t.sleep(0.3)
                                
        rso.dump_log()
            
            
            
            
            
            
            
    def check_buy_order(self,now_price):
        tbo = log.set_log("tightening_buy_order")
        cbo = log.set_log("cancellation_buy_order")
        for bo in self.buy_order:
            b_order = self.buy_order[bo]
            if b_order != 0:
                if b_order["state"] != "done":
                    b_order = self.upbit.get_order(b_order["uuid"])
                    if b_order["state"] == "done":
                        print(f"│  cell {bo}: 구매오더 체결")
                        tbo.add_log({"buy_order": b_order["uuid"],
                                    "buy_coin_num": self.coin_buy_num[bo],
                                    "target_coin_sell_price": self.coin_sell_list[bo],
                                    "target_sell_price": f"{self.coin_sell_list[bo] * self.coin_buy_num[bo]}",
                                    "cell": bo,
                                    "cell_status": "s waiting..."})
                        self.buy_order[bo] = b_order
                        
                        balances = self.upbit.get_balances()
                        for bal in balances:
                            if bal['currency'] in self.config_data["coin_type"]:
                                self.avg_value = bal['avg_buy_price']
                            else:
                                self.avg_value = 0
                        self.buy_count += 1
                        print(f'│  평단가: {self.avg_value}')
                        with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(self.data_data, outfile, indent = 4, allow_unicode = True)
                        
                        
                    elif now_price > float(b_order["price"]) + self.limit * 3:
                        print(f"│  cell {bo}: 구매오더 취소")
                        self.upbit.cancel_order(b_order["uuid"])
                        cbo.add_log({"sell_price": float(b_order["price"]),
                                    "sell_coin_num": self.coin_buy_num[bo],
                                    "cell": bo,
                                    "cell_status": "b waiting...",
                                    "cell_funds": self.cell_funds[bo]})
                        self.coin_sell_list[bo] = 0.0
                        self.coin_buy_list[bo] = 0.0
                        self.coin_buy_num[bo] = 0.0
                        self.sell_order[bo] = 0.0
                        self.buy_order[bo] = 0.0

        tbo.dump_log()
        cbo.dump_log()
        self.data_data["buy_order"] = self.buy_order
            
            
            
            
            
    def check_sell_order(self,now_price):
        tso = log.set_log("tightening_sell_order")
        cso = log.set_log("cancellation_sell_order")
        for so in self.sell_order:
            s_order = self.sell_order[so]
            if s_order != 0.0:
                s_order = self.upbit.get_order(s_order["uuid"])
                if s_order["state"] == "done":
                    if self.sell_type[so] == 'circulation':
                        print(f"│  cell {so}: 순환 판매오더 체결")
                        self.cell_funds[so] = (float(s_order["price"]) * float(s_order["volume"])) - float(self.buy_order[so]["reserved_fee"]) * 2
                        print(f'│  {self.cell_funds[so]}')
                        tso.add_log({"ror": (cal.cal_fee(float(s_order["price"]))/ (self.coin_buy_list[so] - float(self.buy_order[so]["reserved_fee"]))) * 100 - 100,
                                    "sell_price": float(s_order["price"]),
                                    "sell_coin_num": self.coin_buy_num[so],
                                    "cell": so,
                                    "cell_status": "b waiting...",
                                    "sell_type": "circulation",
                                    "cell_funds": self.cell_funds[so]})
                        
                        with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(self.data_data, outfile, indent = 4, allow_unicode = True)
                        
                        self.sell_count += 1
                        self.coin_sell_list[so] = 0.0
                        self.coin_buy_list[so] = 0.0
                        self.coin_buy_num[so] = 0.0
                        self.sell_order[so] = 0.0
                        self.buy_order[so] = 0.0
                        self.sell_type[so] = ''

                    
                    
                    elif self.sell_type[so] == 'nomal':
                        print(f"│  cell {so}: 수익 판매오더 체결")
                        self.cell_funds[so] = (float(s_order["price"]) * float(s_order["volume"])) - float(self.buy_order[so]["reserved_fee"]) * 2
                        print(f'│  {self.cell_funds[so]}')
                        now_revenue = self.upbit.get_balance("KRW")
                        
                        self.yield_list[0] = now_revenue
                        
                        with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                            yaml.dump(self.data_data, outfile, indent = 4, allow_unicode = True)
                        
                        tso.add_log({"ror": (float(s_order["volume"]) * float(s_order["price"])) / (float(self.buy_order[so]["volume"]) * float(self.buy_order[so]["price"])) * 100 - 100,
                                    "sell_price": float(s_order["price"]),
                                    "sell_coin_num": self.coin_buy_num[so],
                                    "cell": so,
                                    "cell_status": "b waiting...",
                                    "sell_type": "nomal",
                                    "cell_funds": self.cell_funds[so],
                                    "yield_t1-1": round(now_revenue / self.yield_list[1] * 100 - 100, 3),
                                    "yield_t1-7": round(now_revenue / self.yield_list[7] * 100 - 100, 3),
                                    "yield_t1-30": round(now_revenue / self.yield_list[30] * 100 - 100, 3),
                                    "yield_t2-1": round(now_revenue - self.yield_list[1], 3),
                                    "yield_t2-7": round(now_revenue - self.yield_list[7], 3),
                                    "yield_t2-30": round(now_revenue - self.yield_list[30], 3)})
                        self.sell_count += 1
                        self.coin_sell_list[so] = 0.0
                        self.coin_buy_list[so] = 0.0
                        self.coin_buy_num[so] = 0.0
                        self.sell_order[so] = 0.0
                        self.buy_order[so] = 0.0
                        self.sell_type[so] = ''
                        self.avg_value = 0.0
                        self.yield_list[0] = now_revenue
                        self.sell_half = False
                    
                    
                    
                elif now_price < float(s_order["price"]) - self.limit * 3:
                    print(f"│  cell {so}: 판매오더 취소")
                    self.upbit.cancel_order(s_order["uuid"])
                    cso.add_log({"sell_price": float(s_order["price"]),
                                "sell_coin_num": self.coin_buy_num[so],
                                "cell": so,
                                "cell_status": "s waiting..."})
                    self.sell_order[so] = 0.0
                    self.data_data['sell_half'] = False
                    self.data_data['circulation'] = False
        tso.dump_log()
        cso.dump_log()
                    
            
            
            
            
    
    
    def oh_dump(self):
        
        
        with open(data_loc, encoding='utf-8') as f:
            data_data_ = yaml.load(f, Loader=yaml.FullLoader)
        
        self.data_data = data_data_
        
        self.data_data['coin_buy_list'] = self.coin_buy_list
        self.data_data['coin_sell_list'] = self.coin_sell_list
        self.data_data['coin_buy_num'] = self.coin_buy_num
        self.data_data['cell_funds'] = self.cell_funds
        self.data_data["buy_order"] = self.buy_order
        self.data_data["sell_order"] = self.sell_order
        self.data_data["sell_type"] = self.sell_type
        self.data_data["avg_value"] = self.avg_value
        self.data_data["b_date"] = self.b_date
        self.data_data["sell_half"] = self.sell_half
        self.data_data["yield_list"] = self.yield_list
        self.data_data["sell_count"] = self.sell_count
        self.data_data["buy_count"] = self.buy_count
        
        
        with open(data_loc, 'w', encoding = 'utf-8') as outfile:
            yaml.dump(self.data_data, outfile, indent = 4, allow_unicode = True)
        
