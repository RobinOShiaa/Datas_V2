'''
Created on 28 Oct 2014

@author: Wenchong
'''

import MySQLdb
import MySQLdb.cursors as cursors
import pandas as pd
import pandas.io.sql as psql
import re
from datetime import datetime
from function.function import chunck_list
from function.function import get_subdir_name


# recommended number of transactions in a single execution
NUM_TRANS = 200

# maximum number of transactions in a single execution
MAX_TRANS = 5000

TEST_DB_NAME = 'raw_db_test'

RAW_DB_NAME = 'raw_db'

WAREHOUSE_NAME = 'datas_test'

LOG_DB_NAME = 'raw_db'
#LOG_DB_NAME = 'datas_test'

#HOST = 'localhost'
HOST = '136.206.19.9'
#HOST = '136.206.48.247'
#HOST = '136.206.48.93'
#HOST = '136.206.48.152'

#HOST_LOG = '136.206.48.124'
#HOST_LOG = '136.206.48.177'
#HOST_LOG = '136.206.48.152'
HOST_LOG = '136.206.48.93'



USERNAME = 'root'
#USERNAME = 'sue' # INSERT OWN
PASSWORD = '123piggy'

#USERNAME = 'root' # INSERT OWN
#PASSWORD = '123abc'


PORT = '3306'


class DBManager(object):
    """Summary
    
    classdocs
    
    Attributes:
        
    """


    def __init__(self, db_name='raw_db', host_name=HOST, user_name=USERNAME, pass_word=PASSWORD):
        """Constructor"""
        self.conn = MySQLdb.connect(db=db_name, host=host_name, user=user_name, passwd=pass_word)#,cursorclass=cursors.SSDictCursor)
        self.cur = self.conn.cursor()
        self.db_name = db_name
        
    
    def __del__(self):
        """Destructor"""
        self.conn.close()
    
    def get_latest_date_record(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result
    
    def get_latest_subdir_names(self, init, dir_path, sql_latest_date):
        """Get sub-folder names that are later than the latest_date"""
        # get all sub-folder names in dir_path
        all_subdir_names = get_subdir_name(dir_path)
        
        # get sub-folder names that are later than the latest_date
        subdir_names = []
        if init:
            # get initial folder name
            subdir_names = [s for s in all_subdir_names if re.match('^\d+_\d+_\d+_init$', s)]
        else:
            # get the date in the latest folder that is uploaded into db
            self.cur.execute(sql_latest_date)
            latest_date = self.cur.fetchone()
            #print latest_date
            if not latest_date:
                latest_date = datetime.strptime('1900_01_01', '%Y_%m_%d')
            else:
                latest_date = re.findall('\d+_\d+_\d+', latest_date[0])#added values when changing cursor class to dict
                latest_date = datetime.strptime(latest_date[0], '%Y_%m_%d')
            
            # get non-initial folder name
            for dir_name in all_subdir_names:
                try:
                    folder_date = datetime.strptime(dir_name, '%Y_%m_%d')
                except:
                    continue
                else:
                    if latest_date < folder_date:
                        subdir_names.append(dir_name)
        
        return subdir_names
    
    def check_table_empty(self, table_name):
        """Checks whether a single table in the raw database is empty before running initial load"""
        sql_check = 'select * from %s order by id desc limit 1;' % table_name
        self.cur.execute(sql_check)
        
        if self.cur.fetchone():
            print 'Table already populated.  Loading updates only...'
            return False
        else:
            return True
    
    def fetch_query(self, sql):
        self.conn.query(sql)
        result = self.conn.store_result()
        fetch = result.fetch_row(maxrows=0,how=1)
        return fetch
    
    

    def fetch_sql_df(self,sql,chunk_df=False):
        if chunk_df==False:
            #temp_conn = MySQLdb.connect(db=RAW_DB_NAME, host=HOST, user=USERNAME, passwd=PASSWORD,cursorclass=cursors.SSDictCursor)
            df = psql.read_sql(sql,self.conn)
            
        
        elif chunk_df==True:
            '''
            sql = sql + ' LIMIT 0, 10000'
            df = psql.read_sql(sql,con=self.conn)
            '''
            
            chunk_size = 1000
            offset = 0
            dfs = []
            while True:
                chunk_sql = sql + " limit %d offset %d" % (chunk_size, offset) 
                dfs.append(psql.read_sql(chunk_sql, con=self.conn))
                offset += chunk_size
                if len(dfs[-1]) < chunk_size:
                    break
                
            df = pd.concat(dfs)
        
            
            

        return df
    
    
    def load_data(self, sql, data, chunck_size=100):
        """Insert or update records
        """
        if data:
            if len(data) >= MAX_TRANS:
                data = chunck_list(data, chunck_size)
                for d in data:
                    self.cur.executemany(sql, d)
            else:
                self.cur.executemany(sql, data)
    
    
    def exec_sql_file(self, sql_file):
        print "\n[INFO] Executing SQL script file: '%s'" % (sql_file)
        statement = ""
    
        for line in open(sql_file):
            if re.match(r'--', line):  # ignore sql comment lines
                continue
            if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
                statement = statement + line
            else:  # when you get a line ending in ';' then exec statement and reset for next statement
                statement = statement + line
                #print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
                try:
                    self.cur.execute(statement)
                except:
                    print "\n[WARN] MySQLError during execute statement"
    
                statement = ""
            
            
            '''
    def insert_records(self, data_list, sql, conn, cur):
        pass
    
    def export_data(self, sql, file_path):
        """"""
        try:
            # get query result set
            self.cur.execute(sql)
            results = self.cur.fetchall()
        except MySQLdb.Error, e:
            # TODO(Wenchong): generate error log and exit programme
            print ('Mysql Error %d: %s' % (e.args[0], e.args[1]))
        else:
            # transform results from 2D tuple to 2D list
            data_list = tuple_to_list(results, 2)
            
            # save dataset into file
            save_to_file(data_list, file_path)

    def get_meta_data(self, file_name, extension):
        return [f.strip(extension).split('_') for f in file_name]
    
    def get_id(self, table_name, id_name, attr_name, attr_list):
        id_list = []
        sql = 'select ' + id_name + ' from ' + table_name + ' where ' + attr_name + ' = %s'
        for d in attr_list:
            self.cur.execute(sql, d)
            result = self.cur.fetchone()
            id_list.append(result[0])
        
        return id_list
    '''
    
    
    
    
        
