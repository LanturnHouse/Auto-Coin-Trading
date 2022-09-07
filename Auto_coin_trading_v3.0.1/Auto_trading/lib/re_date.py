import time as t
import yaml


main_status_loc = "C:/Users/JuJin/Desktop/coin/bridge/status/main_status.yaml"
bridge_loc = "C:/Users/JuJin/Desktop/coin/bridge"


def re_date_f(data_loc):
    with open(data_loc, encoding='utf-8') as f:
        data_data = yaml.load(f, Loader=yaml.FullLoader)
    data_data["b_date"] = t.strftime('%Y-%m-%d', t.localtime(t.time()))
    
    with open(data_loc, 'w', encoding = 'utf-8') as outfile:
            yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)


def check_dr(data_loc):
    with open(data_loc, encoding='utf-8') as f:
        data_data = yaml.load(f, Loader=yaml.FullLoader)
        
    if data_data["b_date"] != t.strftime('%Y-%m-%d', t.localtime(t.time())):
        data_data["b_date"] = t.strftime('%Y-%m-%d', t.localtime(t.time()))
        with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
        return True
    else:
        return False
    
    
    
def auto_dr(data_loc):
    
    
    if check_dr(data_loc):
        with open(data_loc, encoding='utf-8') as f:
            data_data = yaml.load(f, Loader=yaml.FullLoader)
        with open(main_status_loc, encoding='utf-8') as f:
            main_status_data = yaml.load(f, Loader=yaml.FullLoader)
        
        main_status_data["yield_t1-1"] = 0
        main_status_data["yield_t2-1"] = 0
        
        data_data["buy_count"] = 0
        data_data["sell_count"] = 0
        
        if data_data["coin_buy_list"][0] == 0:
            b_list = [data_data["yield_list"][0]]
            for i in range(0,len(data_data["yield_list"]) - 1):
                b_list.append(data_data["yield_list"][i])
            data_data["yield_list"] = b_list
        
        with open(data_loc, 'w', encoding = 'utf-8') as outfile:
                yaml.dump(data_data, outfile, indent = 4, allow_unicode = True)
        
        with open(main_status_loc, 'w', encoding = 'utf-8') as outfile:
                yaml.dump(main_status_data, outfile, indent = 4, allow_unicode = True)

        f = open(f"{bridge_loc}/re date.txt", 'w')
        f.close()
        del f
        
        print(f"│  날짜 갱신 완료.")
    
    
    
