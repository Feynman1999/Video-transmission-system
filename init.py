import configparser
import os , sys

# 返回所有端口对应的地址
def get_addresses():
    config = configparser.ConfigParser()
    config.read(os.path.join(sys.path[0],r'config.ini'))
    secs = config.sections() 
    Dict = {}
    for option in secs:
        tmp = config.items(option)
        tmp_dict = {}
        for item in tmp: # item是二元组
            tmp_dict[item[0]] = item[1]
        Dict[option] = tmp_dict 
    return Dict

# client_address = [] # 元素是元组
# for i in range(1,3): # 2个client
#     client_address.append((address_dict['client'+str(i)]['host'],int(address_dict['client'+str(i)]['port'])))
