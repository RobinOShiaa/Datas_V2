'''
Created on 5 Nov 2014

@author: Wenchong
'''


from datas.functions.functions import *


periods = []
periods.append(['url', 'none/generated by eurostat_pig_periods.py'])
periods.append(['year month'])

years = range(2007, 2015)
months = range(1, 13)

for y in years:
    row = []
    for m in months:
        row.append('ck_%s%s' % (y, '{:0>2d}'.format(m)))
    periods.append(row)


file_path = './../../output/eurostat/periods_generated.csv'
delete_file(file_path)
save_to_file(periods, file_path)


print "finished..."



