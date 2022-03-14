'''
Created on 24 Oct 2014

@author: Wenchong
'''


import re
from selenium import webdriver
from datas.functions.functions import join_list


def get_options(attr):
    dropdown_box = browser.find_element_by_id(attr)
    options = [x for x in dropdown_box.find_elements_by_tag_name('option')]
    opt_values = []
    
    for option in options:
        opt_values.append(str(option.get_attribute('value')))

    return opt_values


# url for partners part 1 & part 2
bookmark_url = ['http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016894_QID_-4E7FF8C6_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016894FLOW,2;DS-016894PARTNER,CN;DS-016894PRODUCT,0203;DS-016894INDICATORS,QUANTITY_IN_100KG;&rankName1=PARTNER_1_2_-1_2&rankName2=PRODUCT_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=INDICATORS_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23',
                'http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-016894_QID_-552537D_UID_-3F171EB0&layout=PERIOD,L,X,0;REPORTER,L,Y,0;PARTNER,L,Z,0;PRODUCT,L,Z,1;FLOW,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-016894FLOW,2;DS-016894PARTNER,US;DS-016894PRODUCT,0203;DS-016894INDICATORS,QUANTITY_IN_100KG;&rankName1=PARTNER_1_2_-1_2&rankName2=PRODUCT_1_2_-1_2&rankName3=FLOW_1_2_-1_2&rankName4=INDICATORS_1_2_-1_2&rankName5=PERIOD_1_0_0_0&rankName6=REPORTER_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&time_most_recent=false&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23']
dir = './../../output/eurostat/'

for i in range(len(bookmark_url)):
    # get periods, reporters & partners from web
    period_list = []
    reporter_list = []
    partner_list = []
    
    browser = webdriver.Firefox()
    browser.get(bookmark_url[i])
    
    partner_list = get_options('selectid_0')
    
    headers = browser.find_elements_by_xpath('//span[starts-with(@id, "LABEL_")]')
    for header in headers:
        res = str(header.get_attribute('title'))
        mat = re.match('^\d+ - [A-Z][a-z]+. \d+$', res)
        if mat:
            period_list.append([res])
        else:
            reporter_list.append(res.split(' ')[0])
    
    browser.quit()
    print partner_list
    
    # extract data from file
    num_reporters = len(reporter_list)    
    count = 0
    index = 0
    indicator = ''
    data = []
    data_list = []

    
    in_file = open('%sDS-016894-part%s.csv' % (dir, i+1), 'r')
    
    for row in in_file:
        row = row.strip('\n').split(',')
        
        if count >= 1 and count <= num_reporters:
            data_list.append(row[1:])
            count += 1
        elif row[0] == 'REPORTER/PERIOD':
            count += 1
        elif row[0] == 'INDICATORS':
            indicator = row[1]
        
        if count > num_reporters:
            flag = 0
            for row in data_list:
                for j in range(len(row)):
                    if flag == 1:
                        data[j].append(row[j])
                    else:
                        data.append([row[j]])
                flag = 1
            
            data = join_list(period_list, data)
            
            url = 'url, %s' % (bookmark_url[i])
            path = '%sPIG_%s_%s.csv' % (dir, partner_list[index/2], indicator)
            index += 1
            
            out_file = open(path, 'w')
            out_file.write(url)
            out_file.write('\n')
            out_file.write(', '.join(reporter_list))
            out_file.write('\n')
            
            for row in data:
                out_file.write(', '.join(row))
                out_file.write('\n')
                
            out_file.close()
            
            data = []
            data_list = []
            count = 0
        # end of if
    # end of inner for-loop
    in_file.close()
# end of outer for-loop


print 'finished...'





