# A python script to extract data from a USDA Plants checklist (http://plants.usda.gov/)
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

DROP TABLE IF EXISTS usda_accepted;
DROP TABLE IF EXISTS usda_not_accepted;
DROP TABLE IF EXISTS usda_synonymy;

CREATE TABLE usda_accepted (
    accept_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    code TEXT NOT NULL UNIQUE, 
    title TEXT, 
    author TEXT, 
    common_name TEXT, 
    family TEXT
);

CREATE TABLE usda_not_accepted (
    syn_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    syn_code TEXT NOT NULL UNIQUE,
    syn_title TEXT, 
    author TEXT, 
    common_name TEXT, 
    family TEXT
);

CREATE TABLE usda_synonymy (
    accept_id INTEGER,
    syn_id INTEGER,
    UNIQUE(accept_id, syn_id)
);
''')
    
fname = input('Enter the name of a USDA Plants checklist .txt file: ')
if len(fname) < 1 : fname = "ak_usda_plants_list.txt"
fh = open(fname,encoding='utf-8')
print (fh.encoding)
#skip the first line (i.e., header) of fh
next(fh)
# create object for counting number of lines processed and set initial value to zero
count = 0

for line in fh:   
    # strips each line of any default white spaces at the end of each line
    # splits each line using "," as the delimiter
    # adds 1 to a count object that keeps track of how many lines are processed
    # sets empty strings in the synonym code  and common name fields to n/a
    line = line.rstrip()
    
    words = line.split('","')
    if words[1] == '':
        words[1] = 'n/a'
    if words[3] == '':
        words[3] = 'n/a'
    count = count + 1
    lst = list()
    # this for loop cleans up the double quotes and encodes each element of words to utf-8 and returns a list
    for i in range(len(words)):      
        wrd = words[i].replace('"','')
        encod = wrd.encode('utf-8')
        lst.append(encod)
 
    print (lst)
    
    # insert data into database tables
    # enter data for accepted names (i.e. where the second element of lst is n/a) into the usda_accepted table
    if lst[1]== b'n/a':
        cur.execute('''INSERT OR REPLACE INTO usda_accepted
        (code, author, common_name, family) VALUES ( ?, ?, ?, ?)''', 
        ( lst[0].decode(), lst[2].decode(), lst[3].decode(), lst[4].decode() ) )
    
    conn.commit()
    
    # enter data for unaccepted names (i.e. where the second element of lst is not n/a) into the usda_not_accepted table
    if not lst[1]== b'n/a':
        cur.execute('''INSERT OR REPLACE INTO usda_not_accepted
        (syn_code, author, common_name, family) VALUES ( ?, ?, ?, ?)''', 
        ( lst[1].decode(), lst[2].decode(), lst[3].decode(), lst[4].decode() ) )

    conn.commit()
 
    # a series of print statements to error check the above code
    # print (lst[0], lst[1], spname[0].encode('utf-8'), spname[1].encode('utf-8'), ssp_var[0].encode('utf-8'), ssp_var[1].encode('utf-8'))
    # print (lst[0], lst[1], sci_name)
    # print(ssp_var)
    # print(ssp_var_raw[0].encode('utf-8'))

print ('There are', count, 'total lines in this file')
print ('All done now. Please run plants_part2.py now. Enter the same text file as input.')
   
