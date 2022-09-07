import dataclasses


@dataclasses
class dc_cal_MA:
    MA_list: list
    graph_type: str


class MA:
    
    def __init__(self,df):
        self.df = df
        
        
        
    def cal_MA(self,MA_range,limit):
        MA_list = []
        value = 0
        for i in range(0,MA_range):
            
            value += float(self.df.at[29 - i, 'close'])
            
            MA_list.append(value / MA_range)
          
        # if self.df.at[29,'close'] < self.df.at[0,'close'] and self.df.at[0,'close'] - self.df.at[29,'close']:
            
        
        
        
        return_ = dc_cal_MA(MA_list, 'up')
        return return_
        