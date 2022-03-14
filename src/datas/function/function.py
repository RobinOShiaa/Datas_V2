'''
Created on 28 Oct 2014

@author: Wenchong
'''
import csv
import glob
import importlib
import os
import re
import shutil
import sys
import xlrd
import zipfile
from datetime import datetime

NETWORK_PATH = 'C://shared qlik//'
#NETWORK_PATH = '//WIN-LKJ095IPO1U//shared qlik//'
#NETWORK_PATH = '//WIN-KM0LCJ0IIQ3//shared_qlik//'
#NETWORK_PATH = 'Z://'

def skip_num_generator(start_num, end_num, skip_num, file):
    with open(file, 'a') as out:
        out.write('\n')
        for i in xrange(start_num, end_num, skip_num):
            out.write('%s,' % str(i))


def get_project_root():
    """Get absolute path of the project root
    
    """
    root = os.getcwd()
    root = root[:root.find('src\\')]
    
    return root


# the path of the eclipse project
ROOT_PATH = get_project_root()


def is_number(string):
    """Check if a string is a number
    
    Check if the given string is either an int or a float.
    """
    try:
        float(string)
    except:
        return False
    else:
        return True


def create_list(n, dim=2):
    """Create a list of list with fixed length
    
    Create an empty fixed length list of sub-lists with given
    dimension.
    
    Args:
        n: Length of the list
        dim: dimension of the list, by default it's a 2D list.
    
    Returns:
        An empty fixed length list of sub-lists with specified
        dimension. For example:
        
        n = 5
        dim = 2
        
        This function returns:
        
        [[], [], [], [], []]
    """
    if dim == 2:
        return map(lambda _: [], range(n))
    elif dim == 3:
        return map(lambda _: [[]], range(n))
    else:
        raise ValueError, 'create_list Error: not handled argument value of dim'


def chunck_list(mylist, n):
    """Chunck a list evenly
    
    Chunck a data list to a list of sub-lists with even width.
    
    Args:
        mylist: A list of data
        n: Number of elements in a sub-list.
    
    Returns:
        A list of sub-lists with even width, the length of each
        sub-list is n. For example:
        
        mylist = [3, 1, 5, 7, 6, 8, 9, 2]
        n = 2
        
        This function returns:
        
        [[3, 1], [5, 7], [6, 8], [9, 2]]
    """
    return [mylist[i:i + n] for i in range(0, len(mylist), n)]


def get_valid_chunck_length(length, max_length=30):
    if length <= 0 or max_length <= 0:
        raise ValueError, 'get_valid_chunck_length() error'
    
    if length <= max_length or max_length == 1:
        return length
    
    chunck_length = 0
    for num_chuncks in range(2, length + 1):
        chunck_length = length / num_chuncks
        
        if chunck_length * num_chuncks != length:
            chunck_length += 1
        
        if chunck_length <= max_length:
            break
    
    return chunck_length


def join_list(list1, list2):
    """Join two lists of list to one list
    
    Join the two sub-lists of the given lists with the same index
    to a single sub-list, so as to form a new single list of list.
    
    Args:
        list1: The first list of list.
        list2: The second list of list.
    
    Returns:
        A list of list that joins the two given lists. For example:
        
        list1 = [[1], [2]]
        list2 = [[5, 6], [7, 8]]
        
        This function returns:
        
        [[1, 5, 6], [2, 7, 8]]
    """
    return [a + b for a, b in zip(list1, list2)]


def union_list(list1, list2, pattern, pos='prefix'):
    """Union two lists
    
    Union elements of the two given lists, with the pattern nested
    either as a prefix or a suffix.
    
    Args:
        list1: The elements of which go on the left.
        list2: The elements of which go on the right.
        pattern: Text to be nested in the unioned list.
        pos: The position where the pattern text goes, either prefix
        or suffix.
    
    Returns:
        A list of unioned list, the elements of which are unioned as
        the format specified by pattern and pos. For example:
        
        list1 = [a, b]
        list2 = [1, 2, 3]
        pattern = 'v_'
        pos = 'prefix'
        
        This function returns:
        
        [['v_a1', 'v_a2', 'v_a3'], ['v_b1', 'v_b2', 'v_b3']]
    """
    n = len(list1)
    mylist = create_list(n, dim=2)
    
    for i in range(n):
        for j in range(len(list2)):
            if pos == 'prefix':
                mylist[i].append('%s%s%s' % (pattern, list1[i], list2[j]))
            elif pos == 'suffix':
                mylist[i].append('%s%s%s' % (list1[i], list2[j]), pattern)
            else:
                raise ValueError, 'union_list Error: unhandled argument value of pos'
    
    return mylist
    

def tuple_to_list(data_tuple, dim=2):
    """Transform a tuple to a list
    
    Transform a tuple with certain dimension to a list with the
    same dimension. Allowed dimensions include 1D, 2D and 3D.
    
    Args:
        data_tuple: A tuple with certain dimension.
        dim: The dimension of the data_tuple.
    
    Returns:
        A list transformed from the data_tuple with the same
        dimension with the given tuple. For example:
        
        data_tuple = ((1, 356), ('12', 98), ('egg', 122, 'boo'))
        dimension = 2
        
        This function returns:
        
        [['1', '356'], ['12', '98'], ['egg', '122', 'boo']]
    """
    data_list = []
    
    if dim == 2:
        for row in data_tuple:
            data_list.append([str(r) for r in list(row)])
    elif dim == 1:
        data_list = list(data_tuple)
    elif dim == 3:
        for col in data_tuple:
            col_list = []
            for row in col:
                col.append([str(r) for r in list(row)])
            data_list.append(col_list)
    else:
        # TODO(Wenchong): generate error log and terminate the programme
        raise ValueError, 'tuple_to_list Error: not handled argument value of dim'
    
    return data_list


def replace_nested_symbol(string, symbol_from, symbol_to):
    """Replace symbol_from with symbol_to inside double quotes
    """
    string = re.sub(r'%s(?=[^"]*"(?:[^"]*"[^"]*")*[^"]*$)' % symbol_from, symbol_to, string)
    return string


def replace_non_ascii(string, char):
    """replace non ASCII chars with the given char
    """
    stripped = ((c if 0 < ord(c) < 127 else char) for c in string)
    return ''.join(stripped)


def create_directory(dir_path, dir_title):
    """Create a directory
    
    Create an empty directory named dir_title under the path
    dir_path.
    
    Args:
        dir_path: Directory path to create the directory.
        dir_title: The name of the directory.
    
    Returns:
        Absolute path of the directory. For example:
        
        dir_path = 'C:\dir\'
        dir_title = 'test'
        
        This function creates a directory and returns the
        directory path:
        
        'C:\dir\test\'
    """
    new_path = os.path.join(dir_path, dir_title)
    
    # if the directory does not exist, create the directory
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    
    return '%s\\' % (new_path)


def delete_directory(dir_path):
    """Delete a directory
    
    Delete an empty/non-empty directory with the full path
    dir_path.
    
    Args:
        dir_path: The full path of the directory.
    """
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)


def delete_file(file_path):
    """Delete a file
    
    Delete a file with the full path of the file.
    
    Args:
        file_path: The full path of the file.
    """
    if os.path.isfile(file_path):
        os.remove(file_path)


def save_to_file(file_path, data_list):
    """Save a dataset to file with write mode
    
    Save a 2D list of strings to a given file.
    
    Args:
        data_list: A 2D list of strings
        file_path: The file path to save the data_list.
    """
    try:
        out_file = open(file_path, 'w')
        for row in data_list:
            out_file.write(','.join(row))
            out_file.write('\n')
    except Exception as err:
        exc_info = sys.exc_info()
        raise Exception('datas.function.function.save_to_file() error:', exc_info[0], exc_info[1], exc_info[2])
    else:
        out_file.close()
        print ('Succeeded writing data into file: %s' % (file_path))


def save_to_file_append(file_path, data_list):
    """Save a dataset to file with append mode
    
    Save a 2D list of strings to a given file.
    
    Args:
        data_list: A 2D list of strings
        file_path: The file path to save the data_list.
    """
    try:
        if os.path.isfile(file_path):
            out_file = open(file_path, 'a')
        else:
            out_file = open(file_path, 'w')
        
        for d in data_list:
            out_file.write(', '.join(d))
            out_file.write('\n')
    except Exception as err:
        exc_info = sys.exc_info()
        raise Exception('datas.function.function.save_to_file_append() error:', exc_info[0], exc_info[1], exc_info[2])
    else:
        out_file.close()
        print ('Succeeded writing data into file: %s' % (file_path))



def save_error_to_log(folder_name, msg_list):
    """Store the error message into the log file with append mode
    """
    dir_title = datetime.now().strftime('%Y_%m_%d')
    dir_path = '%slog\\%s' % (NETWORK_PATH, folder_name)
    dir_path = create_directory(dir_path, dir_title)
    file_path = '%slog.csv' % dir_path
    
    save_to_file_append(file_path, msg_list)


def read_from_file(file_path):
    """Read data from file
    
    Read data from the given file.
    
    Args:
        file_path: The file path to read the data from.
    
    Returns:
        A list of sub-lists, each sub-list of which stores a whole
        line in the file. For example:
        
        The given file reads:
        
        url, http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
        region_code, region_name
        AD, Andorra
        AE, United Arab Emirates
        AF, Afghanistan
        
        This function returns:
        
        [['url', 'http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2'],
         ['region_code', 'region_name'],
         ['AD', 'Andorra']
         ['AE', 'United Arab Emirates']
         ['AF', 'Afghanistan']]
    """
    data_list = []
    
    try:
        in_file = open(file_path, 'r')
        
        for row in in_file:
            row = row.strip('\n').split(', ')
            data_list.append(row)
    except Exception as err:
        exc_info = sys.exc_info()
        raise Exception('datas.function.function.read_from_file() error:', exc_info[0], exc_info[1], exc_info[2])
    else:
        in_file.close()
        print ('Succeeded reading data from file: %s' % (file_path))
    
    return data_list


def transform_excel_to_csv(xls_file,csv_name):
    """Transform data from excel to csv
    """
    b = xlrd.open_workbook(xls_file)
    s = b.sheet_by_index(0)
    bc = open(csv_name + '.csv','w')
    bcw = csv.writer(bc,csv.excel)
    for row in range(s.nrows):
        this_row = []
        for col in range(s.ncols):
            val = s.cell_value(row,col)
            
            'if cell is unicode'
            if s.cell(row,col).ctype == 1:
                if val == u'\u2015':
                    val = '-'
                else:
                    # when val == u'\uff1a'
                    val = replace_non_ascii(val, ':')
            elif s.cell(row,col).ctype == 3:
                val = xlrd.xldate_as_tuple(val,b.datemode)
                val = list(val)
                val[1] = str(val[1]).zfill(2)
                val = [str(v) for v in val[:2]]
                val = ''.join(val)
            
            this_row.append(val)
        # end of inner for-loop
        
        bcw.writerow(this_row)
    # end of outter for-loop
        
    bc.close()


def get_subdir_path(path, pattern='*'):
    current_path = os.getcwd()
    
    os.chdir(path)
    dir_list = [d[0] for d in os.walk(path) if re.match(pattern, d[0].split('\\')[-1])]
    os.chdir(current_path)
    
    return dir_list


def get_subdir_name(path):
    return next(os.walk(path))[1]


def get_all_subdir_paths(dir_path):
    return [s[0] for s in os.walk(dir_path)]


def get_file_paths(path, pattern='*', extension='.csv'):
    """Get all file paths
    
    Get all file paths with the given pattern in the given path
    """
    file_list = []
    ext = pattern + extension
    
    current_path = os.getcwd()
    
    os.chdir(path)
    file_list += [os.path.realpath(e) for e in glob.glob(ext)]
    #file_list = [f.split('\\')[-1] for f in file_list]
    
    os.chdir(current_path)
    
    return file_list


def get_file_name(path, pattern='*', extension='.csv'):
    """Get all file names
    
    Get all file names with the given pattern in the given path
    """
    file_list = []
    ext = pattern + extension
    
    current_path = os.getcwd()
    
    os.chdir(path)
    file_list += [os.path.realpath(e) for e in glob.glob(ext)]
    file_list = [f.split('\\')[-1] for f in file_list]
    
    os.chdir(current_path)
    
    return file_list


def save_download_file(download_path, dest_file):
    """Save downloaded file as the given file
    
    Save the newly downloaded file to a new place with the given file name.
    """
    newest_file = get_download_file_name(download_path)
    
    try:
        # move the file to dest_file
        os.rename(newest_file, dest_file)
    except Exception as err:
        exc_info = sys.exc_info()
        raise Exception('datas.function.function.save_download_file() error:', exc_info[0], exc_info[1], exc_info[2])


def move_download_file(download_path, dest_path):
    """Move downloaded file to the given path
    
    Move the downloaded file to the new place with its original file name.
    """
    newest_file = get_download_file_name(download_path)
    
    try:
        dest_file = dest_path + newest_file.split('\\')[-1]
        os.rename(newest_file, dest_file)
    except Exception as err:
        exc_info = sys.exc_info()
        raise Exception('datas.function.function.move_download_file() error:', exc_info[0], exc_info[1], exc_info[2])


def get_download_file_name(download_path):
    """Get downloaded file name
    
    Return the newly downloaded file name.
    """
    try:
        # get the current working dir
        current_path = os.getcwd()
        
        # switch working dir to download dir
        os.chdir(download_path)
        
        files = filter(os.path.isfile, os.listdir(download_path)) # get all files in the download dir
        files = [os.path.join(download_path, f) for f in files] # add path to each file
        files.sort(key=lambda x: os.path.getmtime(x)) # sort files in download time order
        newest_file = files[-1] # get the latest downloaded file
        
        # switch working dir to previous working dir
        os.chdir(current_path)
        
        # return the file name
        print newest_file
        return newest_file
    except Exception as err:
        exc_info = sys.exc_info()
        raise Exception('datas.function.function.get_download_file_name() error:', exc_info[0], exc_info[1], exc_info[2])


def unzip(source_file, dest_path):
    '''Unzip a .zip file
    
    Extract all contents of source_file to dest_path.
    '''
    try:
        with zipfile.ZipFile(source_file) as zf:
            zf.extractall(dest_path)
    except Exception as err:
        exc_info = sys.exc_info()
        raise Exception('datas.function.function.unzip() error:', exc_info[0], exc_info[1], exc_info[2])


def get_module_references(module_name_file):
    """Get the references of the modules to be invoked.
    """
    out_file = open(module_name_file, 'r')
    rows = out_file.readlines()
    
    module_names = [r.strip() for r in rows]
    
    out_file.close()
    
    # get module references by module names
    module_refs = []
    for mod_name in module_names:
        module_refs.append(importlib.import_module(mod_name))
    
    return module_refs




