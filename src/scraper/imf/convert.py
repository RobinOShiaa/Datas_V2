'''
Created on 2 Dec 2014

@author: Suzanne
'''
import csv
import xlrd
import binascii



def csv_from_excel(in_file, out_file, sheet):
    wb = xlrd.open_workbook(in_file)
    sh = wb.sheet_by_name(sheet)
    your_csv_file = open(out_file, 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
  
    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))
  
    your_csv_file.close()
    

if __name__ == '__main__':
    #in_file = "/users/suzanne/desktop/Exchange_Rate_Report2014-11-25.xls"
    #in_file = "/users/suzanne/desktop/Exchange_Rate_Report2014-11-25.xlsx"
    #out_file = "/users/suzanne/desktop/ERRFixed.csv"
    #in_file = '%stest_test.xls' % OECD_PATH
    #out_file = '%stest_test.csv' % OECD_PATH
    
    ''' try to recover excel file header format here '''
    in_file = '/users/suzanne/workspace/DATAS_Code/output/imf/Exchange_Rate_Report2014-11-25.xls'
    out_file = '/users/suzanne/workspace/DATAS_Code/output/imf/Exchange_Rate_Report2014-11-25_new.xls'
    data = []
    try:
        ifile = open(in_file, 'rb')
        ofile = open(out_file, 'wb')
        
        bof = 'ssssss0x8090x80x00x100x00x0'
        #bof = '0908100000061000BB0DCC0700000000'
        #bof = '0080908000100000'
        #bof = ''.join(format(ord(c), '08b') for c in bof)
        #bof = binascii.a2b_uu(bof)
        count = 0
        for row in ifile:
            #row = row.strip('\n').split(', ')
            data.append(row)
            #if count == 0:
                #row[0]=bof
                #ofile.write(bof)
                #row = '0600H\n'
                #row.replace('\xef\xbb\xbf', bof)
                #row.lstrip('\xef\xbb\xbf')
                #row = row[12:]
                #print row
            #ofile.write(row)
            #count += 1
        data[0] = bof
        for d in data:
            ofile.write(d)#(binascii.b2a_uu(d))
            print d
    except IOError:
        # TODO(Wenchong): generate error log and exit programme
        print ('File Error: can\'t find file or read data')
    else:
        ifile.close()
        ofile.close()
        print ('Succeeded reading data from file: %s' % (in_file))
    #print data
    
    '''
    data = []
    with open(in_file, 'r') as input:
        data = input.read()
    print data
    '''
    
    ''' convert recovered excel file to csv file '''
    in_file = '/users/suzanne/workspace/DATAS_Code/output/imf/Exchange_Rate_Report2014-11-25_new.xls'
    out_file = '/users/suzanne/workspace/DATAS_Code/output/imf/Exchange_Rate_Report2014-11-25.csv'
    sheet = 'EXCHANGE_RATE_REPORT'
    csv_from_excel(in_file, out_file, sheet) #unsupported format or corrupt file
    
    print 'finished...'