'''
Created on 3 Feb 2016

@author: Suzanne
'''
import os
import subprocess
import sys
from datas.function.function import save_error_to_log

def scrape():
    
    subprocess.call(['RScript', 'comtrade_2_dairy_2013_2015.R'])
    
#     command = 'Rscript'
#     path2script = "comtrade_2_dairy_2013_2015.R"
#     cmd = [command, path2script]
#     x = subprocess.check_output(cmd, universal_newlines=True)
#     print x
    
#     progs = ["comtrade_2_dairy_2013_2015.R"]#,"comtrade_2_meat_2010_2015.R"]
#     for prog in progs:
#         try:
#             os.system(prog)
#             
#         except Exception as err:
#             exc_info = sys.exc_info()
#             error_msg = 'auto_run() scrape error at %s:\n' % prog
#             msg_list = [['comtrade'],[error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
#             print msg_list
#             save_error_to_log('monthly', msg_list)
#         else:
#             success_msg = 'auto_run() scraped successfully\n'
#             msg_list = [['comtrade'],[success_msg]]
#             save_error_to_log('monthly', msg_list)
        
if __name__ == '__main__':
    scrape()