import math

def cal_fee(arg):
    arg = arg - arg * 0.0005
    l_arg = str(arg).split(".")
    final = l_arg[0] + "." +  l_arg[1][:2]
    del l_arg
    del arg
    return float(final)

def list_zero_check(alist):
    count = 0
    for i in alist:
        if i != 0.0:
            count = count + 1
    return count

def cal_sell_coin_num(num):
    l_num = str(num).split(".")
    final = l_num[0] + "." +  l_num[1][:8]
    del l_num
    del num
    return float(final)

