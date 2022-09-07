from matplotlib.pyplot import close
import pyupbit




class pyupbit_cal:

    def __init__(self, responsiveness, coin_type):
        self.asking_price = 0
        self.coin_type = coin_type
        self.responsiveness = responsiveness



    
    # def limit_check(self):
        
    #     df = pyupbit.get_ohlcv(self.coin_type,interval = 'minute5' ,count = 20)
    #     df = df.reset_index()
    #     close_list = []
    #     for j in range(0,20):
    #         close_list.append(df.at[j ,"close"])
    #     c_mm = max(close_list) - min(close_list)
        
    #     tick_value = c_mm / self.responsiveness
    #     if tick_value <= self.asking_price * 2:
    #         tick_value = self.asking_price * 2
        
    #     del close_list
    #     return tick_value



    def limit_check(self):
            
        df = pyupbit.get_ohlcv(self.coin_type,interval = 'minute5' ,count = 20)
        df = df.reset_index()
        max_list = []
        min_list = []
        for i in range(0,20):
            max_list.append(df.at[i, "high"])
            min_list.append(df.at[i, "low"])
        c_mm = max(max_list) - min(min_list)
        return (c_mm / self.responsiveness)



    def get_asking_price(self,now_price):
        """호가단위 게산"""
        if now_price < 0.1:
            self.asking_price = 0.0001
            return 0.0001
        elif now_price < 1:
            self.asking_price = 0.001
            return 0.001
        elif now_price < 10:
            self.asking_price = 0.01
            return 0.01
        elif now_price< 100:
            self.asking_price = 0.01
            return 0.1
        elif now_price < 1000:
            self.asking_price = 1
            return 1
        elif now_price < 10000:
            self.asking_price = 5
            return 5
        elif now_price < 100000:
            self.asking_price = 10
            return 10
        elif now_price < 500000:
            self.asking_price = 50
            return 50
        elif now_price < 1000000:
            self.asking_price = 100
            return 100
        elif now_price < 2000000:
            self.asking_price = 500
            return 500
        else:
            self.asking_price = 1000
            return 1000