# A python script to extract titles from a USDA Plants custom checklist (http://plants.usda.gov/)
# Uses Python 3
# Requires DB Browser for SQLite. Download install package here for free: http://sqlitebrowser.org/

import sqlite3
import sys
import re

# create database connection to ak_usda_plants_db.sqlite
conn = sqlite3.connect('ak_usda_plants_db.sqlite')
# create database cursor
cur = conn.cursor()

# create three tables in ak_usda_plants_db.sqlite
cur.executescript('''

DROP TABLE IF EXISTS usda_titles;

CREATE TABLE usda_titles (
    title_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    code_ti TEXT NOT NULL UNIQUE, 
    title_ti TEXT
);
''')
    
fname = input('Enter the name of a USDA Plants checklist with titles: ')
if len(fname) < 1 : fname = "ak_plant_list_with_titles.txt"
fh = open(fname,encoding='utf-8')
print (fh.encoding)
#skip the first line (i.e., header) of fh
next(fh)
# create object for counting number of lines processed and set initial value to zero
count = 0
count2 = 0
# create object for counting the number of genus only records and set initial value to zero
cnt_g = 0

for line in fh:   
    # strips each line of any default white spaces at the end of each line
    # splits each line using "," as the delimiter
    # adds 1 to a count object that keeps track of how many lines are processed
    # sets empty strings in the synonym code  and common name fields to n/a
    line = line.rstrip()
    
    words = line.split('","')[:3]
    if words[1] == '':
        words[1] = 'n/a'
    if words[2] == '':
        words[2] = 'n/a'
    count = count + 1
    lst = list()
    # this for loop cleans up the double quotes, strips default whitespace, and encodes each element of words to utf-8 and returns a list
    for i in range(len(words)):      
        wrd = words[i].replace('"','')
        wrd = wrd.rstrip()
        encod = wrd.encode('utf-8')
        lst.append(encod)
    count2 = count2 + 1
    # grabs the second element of genus_spp which is the scientific name
    genus_spp = lst[2].decode().split(' ')
    # splits the genus_spp on white space, decodes to bytes
    # takes the first two elements the first being genus, the second species.
    # for genus only records the second elements includes the first word of the author.
    #spname = genus_spp.decode().split(' ')[:2]
    
    # finds instances where the second element of the spname is not all lowercase
    # in these instances changes the second element to "genus_only" and adds 1 to the count object cnt_g
    if len(genus_spp) == 1:
        cnt_g = cnt_g + 1
        lst[2] = lst[2] + b' sp.'
        #spname[1] = 'sp.'
        #print(spname[0].encode('utf-8'), spname[1].encode('utf-8'))
    
    print (lst)
    
    # insert data into database tables
    # enter data for accepted names (i.e. where the second element of lst is n/a) into the usda_accepted table
    if lst[1]== b'n/a':
        cur.execute('''INSERT OR REPLACE INTO usda_titles
        (code_ti, title_ti) VALUES ( ?, ?)''', 
        ( lst[0].decode(), lst[2].decode() ) )
    
    conn.commit()
    
    # enter data for unaccepted names (i.e. where the second element of lst is not n/a) into the usda_not_accepted table
    if not lst[1]== b'n/a':
        cur.execute('''INSERT OR REPLACE INTO usda_titles
        (code_ti, title_ti) VALUES ( ?, ?)''', 
        ( lst[1].decode(), lst[2].decode() ) )

    conn.commit()
 
    # a series of print statements to error check the above code
    # print (lst[0], lst[1], spname[0].encode('utf-8'), spname[1].encode('utf-8'), ssp_var[0].encode('utf-8'), ssp_var[1].encode('utf-8'))
    # print (lst[0], lst[1], sci_name)
    # print(ssp_var)
    # print(ssp_var_raw[0].encode('utf-8'))

print ('There are', cnt_g, 'genus only records')
print ('There are', count, 'total lines in this file')
print ('Actually, there are', count2, 'total lines in this file')
print ('All done now.')
   
