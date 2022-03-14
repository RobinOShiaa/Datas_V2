'''
Author: Conor 
Date created: 11/12/14
'''

in_file = open('wasde-01-10-2003.txt', 'r')

txt_lines =  in_file.readlines()

in_file.close()
line_num = 0
for txt_line in txt_lines:
    if(txt_line[0] == '='):
        print txt_lines[line_num + 1].strip() 
    line_num += 1    