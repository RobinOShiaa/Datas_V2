'''
Created on 14 Nov 2014

@author: Wenchong

This code is for combining data in separate files with
the same prodmilk and unit into a single files
'''


from datas.functions.functions import *
from datas.web.scraper import *


if __name__ == '__main__':
    title_path = EUROSTAT_PATH + 'cows_milk_monthly/title_options/'
    
    # get promilk titles
    prodmilk = read_from_file('%sprodmilk.csv' % title_path)
    prodmilk = prodmilk[2:]
    prodmilk = [p[1] for p in prodmilk]
    
    # get unit titles
    unit = read_from_file('%sunit.csv' % title_path)
    unit = unit[2:]
    unit = [u[1] for u in unit]
    
    # input file path
    folder_name = '2014_11_17_by_year'
    dir_path_in = '%scows_milk_monthly/%s/' % (EUROSTAT_PATH, folder_name)
    
    # output file path
    folder_name = datetime.now().strftime('%Y_%m_%d')
    dir_path_out = '%scows_milk_monthly/' % (EUROSTAT_PATH)
    dir_path_out = create_directory(dir_path_out, folder_name)
    
    extension = '.csv'
    
    # combine data with the same prodmilk and unit into a single file
    for prod in prodmilk:
        for unt in unit:
            # get all file names with the same prodmilk and unit
            pattern = '*%s_%s' % (prod, unt)
            file_names = get_file_name(dir_path_in, pattern, extension)
            
            # construct full output file path
            is_file_exist = False
            file_path = file_names[0].split('_')
            file_path = '_'.join(file_path[1:])
            file_path = dir_path_out + file_path
            
            # for eache file name, store the data into
            # a single file with full path file_path
            for file in file_names:
                data_list = read_from_file(dir_path_in + file)
                
                # if file created, skip the headers
                if is_file_exist:
                    data_list = data_list[2:]
                
                save_to_file_append(file_path, data_list)
                
                is_file_exist = True
    
    
    print 'finished...'



