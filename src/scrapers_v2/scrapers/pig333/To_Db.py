'''''''''''
import MySQLdb

db = MySQLdb.connect(host='136.206.19.9',user='datasdev',passwd='123piggy',db='datas_development')

#You need a cursor to execute queries on the database
cur = db.cursor()
print("READING DATA")
# Reading data
def read_data(cursor):
    query  = "SELECT pig333 FROM michael_test;"
    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)


read_data(cur)

'''''


from datetime import date, datetime
with open('.\\csv_files\\2019-07-08_15-05-18.csv') as f:
    print(''.join(['=' for x in range(0, 40)]))
    print("WRITING DATA")
    line = f.readline()
    while line:
        line = f.readline()
        i = 0
        entries = line.split(',')
        print('\n')
        tup = []
        while i < len(entries):

            if i == 2:
                date = (datetime.strptime(entries[i].replace('"',''), '%d-%b-%Y').date())
                tup.append(date.strftime('%d-%b-%Y'))
            elif i == 5:

                tup.append(entries[i].split()[0][1:])

            else:

                tup.append(entries[i][1:len(entries[i])-1])
            i+=1
        print(tuple(tup))
        print(tup)
        insert_query = "INSERT INTO pig333(Continent,Country,Dayid) VALUES('James',34);"
