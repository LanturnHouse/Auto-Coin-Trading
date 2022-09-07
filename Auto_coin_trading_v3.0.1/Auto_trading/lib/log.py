import yaml

bridge_loc = "C:/Users/JuJin/Desktop/coin/bridge"

class set_log:
    
    def __init__(self,file_name):
        self.log = {}
        self.count = 0
        self.file_name = file_name
    

    def add_log(self,l_dic: dict):
        self.log[self.count] = l_dic
        self.count += 1
        del l_dic
    
    
    def dump_log(self):
        if self.log != {}:
            f = open(f"{bridge_loc}/{self.file_name}.yaml", 'w')
            yaml.dump(self.log, f, indent = 4, allow_unicode = True)
            f.close()
            del f