'''
Created on 9 Jan 2015

@author: Wenchong
'''


from datas.function.function import create_directory
from datas.function.function import get_file_paths
from datas.function.function import replace_nested_symbol
from datas.web.path import WEB_EUROSTAT_PATH


def get_product_id():
    prod_ids = []
    
    dir_path = '%spig_meat_trade\\2015_01_08' % WEB_EUROSTAT_PATH
    file_paths = get_file_paths(dir_path)
    
    for file_path in file_paths:
        in_file = open(file_path, 'r')
        rows = in_file.readlines()
        
        i = 1
        while i < len(rows):
            rows[i] = replace_nested_symbol(rows[i].strip(), ',', '')
            prod_id = rows[i].split(',')[2]
            
            if prod_id not in prod_ids:
                prod_ids.append(prod_id)
            
            i += 1
        
        in_file.close()
    
    i = 0
    while i < len(prod_ids):
        prod_ids[i] = 'ck_%s' % prod_ids[i]
        i += 1
    
    dir_path = create_directory(WEB_EUROSTAT_PATH, 'pig_meat_trade\\title_options')
    
    print "finished..."


if __name__ == '__main__':
    get_product_id()