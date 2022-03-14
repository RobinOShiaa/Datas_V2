'''
Created on 17 Apr 2015

@author: Wenchong
'''


import importlib
import sys
from datetime import datetime
from function.function import get_module_references
from function.function import save_error_to_log
#from datas.db.manager import DBManager
#from datas.db.manager import HOST
#from datas.db.manager import PASSWORD
#from datas.db.manager import RAW_DB_NAME
#from datas.db.manager import USERNAME

class Automator(object):
    """Automator for the load/scrape automation system
    
    Attributes:
    
    """
    
    def __init__(self, folder_name, db_params, module_name_file):
        """Constructor"""
        self.folder_name = folder_name
        self.db_params = db_params
        self.module_name_file = module_name_file
    
    def __del__(self):
        """Destructor"""
        pass
    
    def check_module_names(self):
        """Check whether all modules in the file are valid"""
        out_file = open(self.module_name_file, 'r')
        rows = out_file.readlines()
        
        module_names = [r.strip() for r in rows]
        
        out_file.close()
        
        # import all modules
        for mod_name in module_names:
            #print mod_name
            try:
                mod = importlib.import_module(mod_name)
            except ImportError as err:
                exc_info = sys.exc_info()
                raise ImportError('datas.autosys.automator.check_module_names() error:', exc_info[0], exc_info[1], exc_info[2])
    
    def reload_module_file(self, module_name_file):
        """Destructor"""
        self.module_name_file = module_name_file
  
    def insert_load_date(self,dbm):
        """Insert load date into the load log for updating the warehouse"""
        today = datetime.now()
        rawdb_load_date = datetime.strftime(today, '%Y-%m-%d')
        sql = 'insert ignore into etl_load_log (rawdb_load_date) values ("%s");' % rawdb_load_date
        dbm.cur.execute(sql)
        dbm.conn.commit()    
        
    def check_is_empty(self, dbm):
        sql_check = 'select * from bordbia_dairy_price order by id desc limit 1;'
        dbm.cur.execute(sql_check)
        
        if dbm.cur.fetchone():
            print 'At least one table already contains data.'
            return False
            
        else:
            return True
        
    
    def load_init(self):
        """Load initial data"""
        print 'Start initial load at %s...' % datetime.now()
        
        # get module references by module names
        module_refs = get_module_references(self.module_name_file)
        
        # load modules by module references
        init = True
        for mod in module_refs:
            if 'loader' in mod:
                print '\n****************************************************************'
                try:
                    print 'loading ', mod
                    mod.load(self.db_params, init)
                except Exception as err:
                    # save error message to log file
                    exc_info = sys.exc_info()
                    error_msg = 'load_init() error:'
                    msg_list = [[str(mod)], [error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
                    save_error_to_log(self.folder_name, msg_list)
        
        print 'Finish initial load at %s...' % datetime.now()
    
    
    def auto_run(self):
        """Automate load and scrape"""
        # get module references by module names
        module_refs = get_module_references(self.module_name_file)

        # load modules by module references
        i = 0
        while i < len(module_refs):
            print module_refs[i]
            if 'scraper' in str(module_refs[i]):
                try:
                    print 'scraping ', module_refs[i]
                    module_refs[i].scrape(self.db_params)
                except Exception as err:
                    # save error message to log file
                    exc_info = sys.exc_info()
                    error_msg = '\n\nauto_run() scrape error:'
                    msg_list = [[str(module_refs[i])], [error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
                    save_error_to_log(self.folder_name, msg_list)
            elif 'loader' in str(module_refs[i]):
                try:
                    print 'loading ', module_refs[i]
                    module_refs[i].load(self.db_params)
                except Exception as err:
                    # save error message to log file
                    exc_info = sys.exc_info()
                    error_msg = '\n\nauto_run() scrape error:'
                    msg_list = [[str(module_refs[i])], [error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
                    save_error_to_log(self.folder_name, msg_list)
            else:
                print 'Invalid module'
#             except Exception as err:
#                 # save error message to log file
#                 exc_info = sys.exc_info()
#                 error_msg = '\n\nauto_run() scrape error:'
#                 msg_list = [[str(module_refs[i])], [error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
#                 save_error_to_log(self.folder_name, msg_list)
                
            i += 1
            
        print '\nFinish loading jobs...\n'

        
#         print 'Start loading jobs...\n'
#         
#         # load modules by module references
#         i = 0
#         while i < len(module_refs) - 1:
#             print '\n****************************************************************'
#             # load before scrape to load any data that were scraped last time
#             # which haven't been loaded
#             # may need to be removed
#             try:
#                 print 'loading ', module_refs[i+1]
#                 module_refs[i+1].load(self.db_params)
#             except Exception as err:
#                 # save error message to log file
#                 exc_info = sys.exc_info()
#                 error_msg = 'auto_run() load error:'
#                 msg_list = [[str(module_refs[i+1])], [error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
#                 save_error_to_log(self.folder_name, msg_list)
#             
#             # scrape new data
#             # load new data immediately after scrape
#             try:
#                 print 'scraping ', module_refs[i]
#                 module_refs[i].scrape(self.db_params)
#             except Exception as err:
#                 # save error message to log file
#                 exc_info = sys.exc_info()
#                 error_msg = '\n\nauto_run() scrape error:'
#                 msg_list = [[str(module_refs[i])], [error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
#                 save_error_to_log(self.folder_name, msg_list)
#             else:
#                 try:
#                     print 'loading ', module_refs[i+1]
#                     module_refs[i+1].load(self.db_params)
#                 except Exception as err:
#                     # save error message to log file
#                     exc_info = sys.exc_info()
#                     error_msg = '\n\nauto_run() load error:'
#                     msg_list = [[str(module_refs[i+1])], [error_msg], [str(exc_info[0])], [str(exc_info[1])], [str(exc_info[2]) + '\n\n']]
#                     save_error_to_log(self.folder_name, msg_list)
#             
#             i += 2
#         
#         print '\nFinish loading jobs...\n'


# END OF FILE