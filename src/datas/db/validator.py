'''
Created on 17 Feb 2015

@author: Conor 
'''
import sys
import re
import numpy as np
import pandas as pd
import os
import time
from pandas.util.testing import assert_series_equal
from db.manager import DBManager
from datetime import datetime
from db.manager import HOST_LOG, LOG_DB_NAME, USERNAME, PASSWORD, HOST
from function.function import ROOT_PATH, is_number, chunck_list
from numpy import nan
#from db.loader.oecd.economic_stats_sql_table_generator import table_name

csv_path = ROOT_PATH + 'output_validation\\'
CONORS_IP = '136.206.48.177'
#CONORS_IP = '136.206.48.124'

class Validator(object):
    
    def __init__(self, multi_type,category_name,type_name,value_name,date_name,init=True):
        self.init = init
        self.multi_type = multi_type
        self.category_name = category_name
        self.type_name = type_name
        self.value_name = value_name
        self.date_name = date_name
        
    def csv_table_checker(self,csv_dir,metafile_dir,db,value_element,csv_values_are_str,program_dir,end_row_skip=0):
        #print 'test'
        print 'Validating....'
        #print metafile_dir
        try:
            in_file = open(metafile_dir,'r')
        except:
            print 'Metafile was not found at the specified directory'
            return False    
        
        rows = in_file.readlines()
        #print rows        
        for row_num in xrange(0,5):
            split_row = rows[row_num].split(',')
            if split_row[0].strip() == 'table_name':
                table_name = split_row[1].strip()
            elif split_row[0].strip() == 'db_name':
                db_name = split_row[1].strip()     
            elif split_row[0].strip() == 'column_list':
                column_lst = []
                for col_num in xrange(1,len(split_row)):
                    column_lst.append(int(split_row[col_num].strip()))
            elif split_row[0].strip() == 'rows_skip_list':
                skip_rows_lst = []
                if len(split_row) > 1:
                    for col_num in xrange(1,len(split_row)):
                        try:
                            skip_rows_lst.append(int(split_row[col_num].strip()))
                        except:
                            skip_rows_lst = []    
            elif split_row[0].strip() == 'header_start':
                try:
                    header_row = int(split_row[1].strip())
                except:
                    header_row = None
                    
#                 if split_row[1].strip() =="'test'":
#                     print split_row[1]
#                     header_row = None
#                 else:
#                     print split_row[1]
#                     header_row = int(split_row[1].strip())
            else:
                print 'metafile is not in the correct format'
                return False                    
        in_file.close()
        
        if end_row_skip > 0:
            try: 
                in_csv_file = open(csv_dir,'r')
            except:
                print 'csv file was not found.'     
                return False
            
            csv_rows = in_csv_file.readlines() 
            #print len(csv_rows)
            end_rows_lst = range((len(csv_rows) - 1),((len(csv_rows) - end_row_skip) - 1),-1)
            skip_rows_lst = skip_rows_lst + end_rows_lst
            skip_rows_lst = set(skip_rows_lst)
            #print skip_rows_lst
            in_csv_file.close()
        
        db_sql = 'SELECT * FROM ' + table_name
       
        #print table_name
        
        table_df = db.fetch_sql_df(db_sql,True)
        #table_df = db.fetch_sql_df(db_sql)
        #print table_df
        
        #file_unique = table_df['file'].unique
        #print file_unique()
        
        if isinstance(value_element, list):
            
            temp_lst = []
            for value in value_element:
                temp_col = table_df[table_df['file'] == csv_dir][value]
                #print csv_dir
                #print table_df['file'].unique
                #print table_df[table_df['file'] == csv_dir]
                #print csv_dir
                #print table_df['file'].unique()
                #print csv_dir
                
                temp_lst = temp_lst + temp_col.values.tolist()
            
            value_col = pd.Series(data=temp_lst) 
            value_field = value_element[0]
            #print temp_lst 
                       
        else:
            value_field = value_element
            value_col = table_df[table_df['file'] == csv_dir][value_field]
            #print value_col    
            #print table_df[table_df['file'] == csv_dir]
            #print csv_dir
        #print table_name
        #print skip_rows_lst
        csv_df = pd.read_csv(csv_dir,header=header_row,skiprows=skip_rows_lst,skipinitialspace=True,thousands=',',low_memory=False).dropna(how="all")
        #print csv_df
        
        revised_column_lst = []
        for col in column_lst:
            if col < len(csv_df.columns):
                revised_column_lst.append(col)
               
        subset_csv_df = csv_df[revised_column_lst]
        
        #print subset_csv_df
        #csv_df.to_csv('fullcsv.csv')
        #subset_csv_df.to_csv('csvsubset.csv')
        
        csv_lst = []
        csv_values = subset_csv_df.values
        for row in csv_values:
            for value in row:
                csv_lst.append(value)  
                
        csv_new_df = pd.DataFrame(columns=[value_field])
        
        csv_new_df[value_field] = csv_lst
        
        #print csv_new_df
        #csv_new_df.to_csv(dir_path + 'csv.csv')
        
        csv_dim = subset_csv_df.shape
        #print 'csv_dim: ', csv_dim
        
        if len(csv_dim) == 2:
            csv_value_num = csv_dim[0] * csv_dim[1]
            #print 'csv_value_num: ', csv_value_num
        else:
            csv_value_num = csv_dim[0]
       
        if csv_values_are_str == True:
            #csv_new_df[value_field] = csv_new_df[value_field].replace(to_replace='/[^0-9.]/g',value='',regex=True).convert_objects(convert_numeric=True)
            
            csv_new_df[value_field] = csv_new_df[value_field].replace(to_replace='[^0-9.-]',value='',regex=True).convert_objects(convert_numeric=True)
               

        dbm = DBManager(db_name=LOG_DB_NAME, host_name=HOST, user_name=USERNAME, pass_word=PASSWORD)

        current_time = str(datetime.today())
        csv_count_str = str(csv_value_num)
        table_count_str = str(len(value_col))
        #print csv_value_num, len(value_col)
        
        csv_sum_num = csv_new_df[value_field].sum()
        table_sum_num = value_col.sum()
        
        ##### DE-BUGGING #####
        #print value_col
        #print csv_new_df

        #csv_new_df.to_csv('problem_csv.csv')
        #value_col.to_csv('problem_table.csv')


        #print csv_sum_num
        #print table_sum_num
        #print csv_sum_num - table_sum_num
        ######################
        if csv_sum_num == '':
            csv_sum_num = nan

        csv_sum_str = str(csv_sum_num)
        
        table_sum_str = str(table_sum_num)
        
        if str(csv_sum_num) == 'nan' and str(table_sum_num) == 'nan':
            
            csv_table_match = (csv_value_num == len(value_col))
        else:
            csv_table_match = (csv_value_num == len(value_col)) and (("%.9f" % csv_sum_num) == ("%.9f" % table_sum_num)) 
            #csv_table_match = (csv_value_num == len(value_col)) and (csv_sum_num ==  table_sum_num)
            
        
        if csv_table_match == False and (abs(csv_sum_num - table_sum_num) < 1) and (csv_value_num == len(value_col)):
            
            ordered_csv = csv_new_df[value_field].order()
            ordered_table = value_col.order()
#             print 'csv\n', ordered_csv
#             print 'table\n', ordered_table
            check_equal = (ordered_csv == ordered_table)
            
            #equality_df = pd.DataFrame(data=[ordered_csv,ordered_table,check_equal],columns=['csv','table','equal'])
            
            equality_df = pd.DataFrame()
            equality_df['csv'] = ordered_csv.values
            equality_df['table'] = ordered_table.values
            equality_df['equal'] = equality_df['csv'] == equality_df['table']
            equality_df['diff'] = equality_df['csv'] - equality_df['table']
            #equality_df = pd.concat([ordered_csv,ordered_table,check_equal],axis=1)
            
            equality_df['verdict'] = abs(equality_df['diff']) < 0.00001
            
            equality_df.loc[equality_df['diff'].isnull(),'verdict'] = True
            #print equality_df['verdict']
            limit = all(equality_df['verdict'])
            #print limit
            if limit == True:
                csv_table_match = True
#             false_df = equality_df[equality_df['equal'] == False]
#             
#             false_df.loc[abs(false_df['diff']) < 0.000001,'limit'] 
#             print false_df['limit'].values
#             print false_df['diff'].values
#             false_df['greater'] = false_df
            #print false_df['equal'].
            #df.loc[df[self.value_name] == 0,self.value_name] = np.nan
        #elif csv_table_match == False and (csv_sum_num > 1e14) and (table_sum_num > 1e14):
            #print 'hello'
        
        
        
        if table_sum_str == 'nan':
            
            table_sum_str = None

        if csv_sum_str == 'nan':
            csv_sum_str = None

        if csv_table_match == True:
            csv_table_bool = '1'
        else:
            csv_table_bool = '0'    
        
        sql_log = ('insert into loader_log'
                    '(load_time,database_name,table_name,csv_count,table_count,csv_sum,table_sum,data_match,csv_file_dir,metafile_dir,program_dir)'
                    ' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);')
        #print 'table count: ' + table_count_str
        #print 'table sum: ' + table_sum_str
        
        dbm.cur.executemany(sql_log, [[current_time,db.db_name,table_name,csv_count_str,table_count_str,csv_sum_str,table_sum_str,csv_table_bool,csv_dir,metafile_dir,program_dir]])
        #print dbm.db_name
        dbm.conn.commit()
        
        del dbm
        
        if csv_table_match == True:
            print 'Validation passed'
            return True
        else:
            print 'Validation failed'
            
            return False 
        
        
    def outlier_checker(self,metafile_dir,db,zero_is_null,filter_df=False,filter_str='',n_sd=3):
        print 'Outlier detection running....'
        try:
            in_file = open(metafile_dir,'r')
        except:
            print 'Metafile was not found at the specified directory'
            return False    
        rows = in_file.readlines()
        for row_num in xrange(0,5):
            split_row = rows[row_num].split(',')
            if split_row[0].strip() == 'table_name':
                table_name = split_row[1].strip()
                
        in_file.close()
                
        select_sql = 'SELECT * FROM ' + table_name# + ' where substr(date,1,4) >= "2008"'
               
        table_df = db.fetch_sql_df(select_sql)
        
        
        if filter_df == False:
        
            df = self.diff_cols(table_df, False, 0,zero_is_null)
            df = self.get_value_stats(df,0,False,n_sd)
            df = self.spot_outliers(df, 0)
            
            df = self.diff_cols(df,True,1,zero_is_null)
            
            df = self.get_value_stats(df,1,True,n_sd)
            df = self.spot_outliers(df,1)
            
            
            df =  self.set_standard(df, 1)
                   
            outlier_df = df[(df['verdict1'] == 'event') | (df['verdict1'] == 'mistake') | (df['verdict1'] == 'standard')]
            
            id_values = outlier_df['id'].values
            verdict_values = outlier_df['verdict1'].values
            '''
            for x in xrange(0,len(id_values)):
                update_sql = 'UPDATE ' + db.db_name + '.' + table_name + ' SET outlier_verdict = "' + verdict_values[x] + '" WHERE id = ' + str(id_values[x]) + ';'
                
                db.cur.execute(update_sql)
            db.conn.commit()
            '''
            
            '''
            update_sql_lst = []
            for x in xrange(0,len(id_values)):
                update_sql = 'update ' + db.db_name + '.' + table_name + ' set outlier_verdict = "' + verdict_values[x] + '" where id = ' + str(id_values[x]) + ';'
                update_sql_lst.append(update_sql)
            
            update_sql_lst = chunck_list(update_sql_lst,100)
            
            for row in update_sql_lst:
                for query in row:
                    db.cur.execute(query)
                db.conn.commit()    
            '''
            
            update_sql = 'update ' + db.db_name + '.' + table_name + ' set outlier_verdict = %s where id = %s;'        
            
            data_lst = []
            for x in xrange(0,len(id_values)):
                
                update_data = [verdict_values[x],id_values[x]]
                data_lst.append(update_data)
            
            data_lst = chunck_list(data_lst,500)
            for row in data_lst:
                
                db.cur.executemany(update_sql,row)
                db.conn.commit()       
        
        elif filter_df == True:    
            filter_values = table_df[filter_str].unique()
            #print filter_values
            for filter_value in filter_values:
                #print filter_value
                df = table_df[table_df[filter_str] == filter_value]
                
                df = self.diff_cols(df, False, 0,zero_is_null)
            
                df = self.get_value_stats(df,0,False,n_sd)
                
                df = self.spot_outliers(df, 0)
                
                df = self.diff_cols(df,True,1,zero_is_null)
                
                df = self.get_value_stats(df,1,True,n_sd)
                df = self.spot_outliers(df,1)
                
                
                df =  self.set_standard(df, 1)
                
                
            
                outlier_df = df[(df['verdict1'] == 'event') | (df['verdict1'] == 'mistake') | (df['verdict1'] == 'standard')]
                
                id_values = outlier_df['id'].values
                verdict_values = outlier_df['verdict1'].values
                
                
                update_sql = 'update ' + db.db_name + '.' + table_name + ' set outlier_verdict = %s where id = %s;'        
                
                data_lst = []
                for x in xrange(0,len(id_values)):
                    
                    update_data = [verdict_values[x],id_values[x]]
                    data_lst.append(update_data)
                
                data_lst = chunck_list(data_lst,500)
                for row in data_lst:
                    
                    db.cur.executemany(update_sql,row)
                    db.conn.commit()       
  
        print 'Outliers detection finished'    
            
        
        
        
    def pivot_df(self,df,index_col,category_col,values_col):
        pivot_df = df.pivot_table(index=index_col,columns=category_col,values=values_col)
        return pivot_df
        
    '''    
    def merge_csv(self,file_names,header_row,na_lst,add_column,column_name):
        merged_df = pd.DataFrame()
        date_dirs = os.listdir(os.getcwd())  
        
        for folder in xrange(0,len(date_dirs)):
            if(self.init == True and 'init' in date_dirs[folder]):
                for file_name in file_names:
                    csv_file = pd.read_csv(date_dirs[folder] + '/' + file_name + '.csv',header=header_row,na_values= na_lst)
                    
                    if add_column == 'yes':
                        csv_file[column_name] = file_name.split('_')[3]
                    merged_df = merged_df.append(csv_file)
        return merged_df
            
    def strip_headers(self, df):
        df = df.rename(columns=lambda x: x.strip())
        return df
    
    def describe_df(self,df):
        df_stats = df.describe()
        return df_stats
    
    def compare_dfs(self, df_one,df_two):
        try:
            check_dfs = df_one.sort(axis=1) == df_two.sort(axis=1)
            return check_dfs
        except:
            print 'Cannot compare Dataframes, headers do not match!'    
        #assert_frame_equal(csvdata, csvdata_old)
    '''    
               
    
    def diff_cols(self,df,remove_mistakes,round_num,zero_is_null):
        '''
        revised
        '''
        if zero_is_null == True:
            df.loc[df[self.value_name] == 0,self.value_name] = np.nan
        
        
        
        category_lst = df[self.category_name].unique()
        complete_df = pd.DataFrame() 
        
        if self.multi_type == True:
            if remove_mistakes == False:
                for category in xrange(0,len(category_lst)):
                    type_lst = df[df[self.category_name] == category_lst[category]][self.type_name].unique()
                    for type_element in xrange(0,len(type_lst)):
                        category_df = df[(df[self.category_name] == category_lst[category]) & (df[self.type_name] == type_lst[type_element])].sort([self.category_name,self.type_name,self.date_name])
                        category_df['diff_value' + str(round_num)] = category_df[self.value_name].diff()
                        category_df['prev_value_1' + str(round_num)] = category_df[self.value_name].shift(periods=1)
                        category_df['prev_value_2' + str(round_num)] = category_df[self.value_name].shift(periods=2)
                        category_df['next_value' + str(round_num)] = category_df[self.value_name].shift(periods=-1)
                        #category_df['rolling_std'] = pd.rolling_std(category_df['diff_value'],5,center=True,min_periods=1)
                        #category_df['rolling_mean'] = pd.rolling_mean(category_df['diff_value'],5,center=True,min_periods=1)
                        #category_df['rolling_max'] = pd.rolling_max(category_df['diff_value'],5,center=True,min_periods=1)
                        #category_df['rolling_min'] = pd.rolling_min(category_df['diff_value'],5,center=True,min_periods=1)
                        complete_df = complete_df.append(category_df)
        
            elif remove_mistakes == True:
                                
                for category in xrange(0,len(category_lst)):
                    type_lst = df[df[self.category_name] == category_lst[category]][self.type_name].unique()
                    for type_element in xrange(0,len(type_lst)):
                        category_df = df[(df[self.category_name] == category_lst[category]) & (df[self.type_name] == type_lst[type_element])].sort([self.category_name,self.type_name,self.date_name])
                        #category_df.loc[category_df['verdict' + str(round_num - 1)] != 'mistake','diff_value' + str(round_num)] = category_df[category_df['verdict' + str(round_num - 1)] != 'mistake'][self.value_name].diff() 
                        #category_df.loc[category_df['verdict' + str(round_num - 1)] != 'mistake','prev_value_1' + str(round_num)] = category_df[category_df['verdict' + str(round_num - 1)] != 'mistake'][self.value_name].shift(periods=1)
                        #category_df.loc[category_df['verdict' + str(round_num - 1)] != 'mistake','prev_value_2' + str(round_num)] = category_df[category_df['verdict' + str(round_num - 1)] != 'mistake'][self.value_name].shift(periods=2)
                        #category_df.loc[category_df['verdict' + str(round_num - 1)] != 'mistake','next_value' + str(round_num)] = category_df[category_df['verdict' + str(round_num - 1)] != 'mistake'][self.value_name].shift(periods=-1)
                        category_df['diff_value' + str(round_num)] = category_df[self.value_name].diff()
                        category_df['prev_value_1' + str(round_num)] = category_df[self.value_name].shift(periods=1)
                        category_df['prev_value_2' + str(round_num)] = category_df[self.value_name].shift(periods=2)
                        category_df['next_value' + str(round_num)] = category_df[self.value_name].shift(periods=-1)
                        complete_df = complete_df.append(category_df)
                        
        elif self.multi_type == False:
            if remove_mistakes == False:
                for category in xrange(0,len(category_lst)):   
                    category_df = df[df[self.category_name] == category_lst[category]].sort([self.category_name,self.date_name])
                    category_df['diff_value' + str(round_num)] = category_df[self.value_name].diff()
                    category_df['prev_value_1' + str(round_num)] = category_df[self.value_name].shift(periods=1)
                    category_df['prev_value_2' + str(round_num)] = category_df[self.value_name].shift(periods=2)
                    category_df['next_value' + str(round_num)] = category_df[self.value_name].shift(periods=-1)
                    
                    complete_df = complete_df.append(category_df)
            
            elif remove_mistakes == True:
                for category in xrange(0,len(category_lst)):
                    category_df = df[(df[self.category_name] == category_lst[category])].sort([self.category_name,self.date_name])
                    category_df['diff_value' + str(round_num)] = category_df[self.value_name].diff()
                    category_df['prev_value_1' + str(round_num)] = category_df[self.value_name].shift(periods=1)
                    category_df['prev_value_2' + str(round_num)] = category_df[self.value_name].shift(periods=2)
                    category_df['next_value' + str(round_num)] = category_df[self.value_name].shift(periods=-1)
                    complete_df = complete_df.append(category_df)
        return complete_df
          
    def get_value_stats(self,df,round_num,remove_mistakes,n_sd):
        '''
        revised
        '''
        category_lst = df[self.category_name].unique()          
        
        stats_cols = [self.category_name,self.type_name,'mean','std_dev']
        stats_df = pd.DataFrame(columns=stats_cols)
        
        if self.multi_type == True:
            stats_cols = [self.category_name,self.type_name,'mean' + str(round_num),'std_dev' + str(round_num)]
            stats_df = pd.DataFrame(columns=stats_cols)
            category_type = 0
            #if remove_mistakes == False:
                
            for category in xrange(0,len(category_lst)):
                type_lst = df[df[self.category_name] == category_lst[category]][self.type_name].unique()
                for type_element in xrange(0,len(type_lst)):
                    if remove_mistakes == False:
                        category_df = df[(df[self.category_name] == category_lst[category]) & (df[self.type_name] == type_lst[type_element])].sort([self.category_name,self.type_name,self.date_name]) 
                    elif remove_mistakes == True:
                        category_df = df[(df[self.category_name] == category_lst[category]) & (df[self.type_name] == type_lst[type_element]) & (df['verdict' + str(round_num - 1)] != 'mistake')].sort([self.category_name,self.type_name,self.date_name])
                    area_value = category_lst[category]
                    type_value = type_lst[type_element]
                    mean_value = category_df[self.value_name].diff().mean()
                    std_value = category_df[self.value_name].diff().std()
                    stats_df.loc[category_type] = [area_value,type_value,mean_value,std_value]
                    category_type += 1
            
            
            stats_df['upper_bound' + str(round_num)] = stats_df['mean' + str(round_num)] + (n_sd * stats_df['std_dev' + str(round_num)])
            stats_df['lower_bound' + str(round_num)] = stats_df['mean' + str(round_num)] - (n_sd * stats_df['std_dev' + str(round_num)])
            df = pd.merge(df,stats_df,how='inner',left_on=[self.category_name,self.type_name],right_on=[self.category_name,self.type_name])
            return df
            
            
                
        elif self.multi_type == False:
            stats_cols = [self.category_name,'mean' + str(round_num),'std_dev' + str(round_num)]
            stats_df = pd.DataFrame(columns=stats_cols)
            for category in xrange(0,len(category_lst)):
                if remove_mistakes == False:
                    category_df = df[(df[self.category_name] == category_lst[category])].sort([self.category_name,self.date_name])
                elif remove_mistakes == True:
                    category_df = df[(df[self.category_name] == category_lst[category]) & (df['verdict' + str(round_num - 1)] != 'mistake')].sort([self.category_name,self.date_name])  
                area_value = category_lst[category]
                mean_value = category_df[self.value_name].diff().mean()
                std_value = category_df[self.value_name].diff().std()
                stats_df.loc[category] = [area_value,mean_value,std_value]
            
            stats_df['upper_bound' + str(round_num)] = stats_df['mean' + str(round_num)] + (n_sd * stats_df['std_dev' + str(round_num)])
            stats_df['lower_bound' + str(round_num)] = stats_df['mean' + str(round_num)] - (n_sd * stats_df['std_dev' + str(round_num)])
            
            df = pd.merge(df,stats_df,how='inner',left_on=[self.category_name],right_on=[self.category_name])
            return df
                    
    def spot_outliers(self,df,round_num):
        '''
        revised
        '''
        
        df['outlier' + str(round_num)] = ''
        
        df.loc[(df['diff_value' + str(round_num)] > df['upper_bound' + str(round_num)]),'outlier' + str(round_num)] = 'upper'
        df.loc[df['diff_value' + str(round_num)] < df['lower_bound' + str(round_num)],'outlier' + str(round_num)] = 'lower'
        
        df['verdict' + str(round_num)] = ''
        
        df.loc[(df['outlier' + str(round_num)] == 'upper') | (df['outlier' + str(round_num)] == 'lower'),'verdict' + str(round_num)] = 'Yes'
        
        df.loc[(df['outlier' + str(round_num)] == 'upper') & ((df['next_value' + str(round_num)] - df[self.value_name]) < df['lower_bound' + str(round_num)]),'verdict' + str(round_num)] = 'mistake'
        df.loc[(df['outlier' + str(round_num)] == 'lower') & ((df['next_value' + str(round_num)] - df[self.value_name]) > df['upper_bound' + str(round_num)]),'verdict' + str(round_num)] = 'mistake'
        
        df.loc[df['verdict' + str(round_num)] == 'Yes','verdict' + str(round_num)] = 'event'
        
        df['verdict_m1' + str(round_num)] = df['verdict' + str(round_num)].shift(periods=1)
        
        df.loc[(df['verdict_m1' + str(round_num)] == 'mistake') & (df['outlier' + str(round_num)] == 'upper') & ((df[self.value_name] - df['prev_value_2' + str(round_num)]) < df['upper_bound' + str(round_num)]) & ((df[self.value_name] - df['prev_value_2' + str(round_num)]) > df['lower_bound' + str(round_num)]),'verdict' + str(round_num)] = 'untrue'
        df.loc[(df['verdict_m1' + str(round_num)] == 'mistake') & (df['outlier' + str(round_num)] == 'lower') & ((df[self.value_name] - df['prev_value_2' + str(round_num)]) < df['upper_bound' + str(round_num)]) & ((df[self.value_name] - df['prev_value_2' + str(round_num)]) > df['lower_bound' + str(round_num)]),'verdict' + str(round_num)] = 'untrue'
        
        
        return df
        
            
        
    
    
    def date_cols(self,df,date_name):
        df['yearweek'] = df[date_name].apply(lambda x: x.strftime('%Y%W'))
        df['year'] = df[date_name].apply(lambda x: x.strftime('%Y'))
        df['month'] = df[date_name].apply(lambda x: x.strftime('%m'))
        df['yearmonth'] = df[date_name].apply(lambda x: x.strftime('%Y%m'))
        
        return df
    

    def set_standard(self,df,round_num):
        df.loc[(df['verdict' + str(round_num)] != 'mistake') & (df['verdict' + str(round_num)] != 'event'),'verdict' + str(round_num)] = 'standard'
        
        return df
    
    
    
    #def eigen_values(self,):

