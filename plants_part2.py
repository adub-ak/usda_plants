# Part 2 of plants.py 
# A second for loop to select data from the database and insert into usda_synonymy table
# Uses as input the same text file used in plants.py

import sqlite3
import sys
import re

conn = sqlite3.connect('ak_usda_plants_db.sqlite')
cur = conn.cursor()

fname = input('Enter the name of a USDA Plants checklist .txt file: ')
if len(fname) < 1 : fname = "ak_usda_plants_list.txt"
fh = open(fname,encoding='utf-8')
print (fh.encoding)
#skip the first line (i.e., header) of fh
next(fh)

for line in fh:
    # strips each line of any default white spaces at the end of each line
    # cleans up the double quotes, replacing them with empty strings
    # splits each line using comma as the delimiter
    linez = line.rstrip()
    line = line.replace('"','')
    wordsz = line.split(',')
    
    # skips over accepted taxa, i.e., where the second element of words is null
    if wordsz[1] == '': continue
        # print(wordsz[0],wordsz[1])
    # for taxa that are not accepted selects the ids from the usda_accepted table and usda_not_accepted table
    # inserts the related ids into the usda_synonymy table
    else:
        
        accept_code = (wordsz [0],)
        syny_code = (wordsz[1],)
        print (accept_code,syny_code, 'hey there')
        
        cur.execute('SELECT accept_id FROM usda_accepted WHERE code = ? ', accept_code)
        accept_id = cur.fetchone()[0]
        
        cur.execute('SELECT syn_id FROM usda_not_accepted WHERE syn_code = ? ', syny_code)
        syny_id = cur.fetchone()[0]
        
        cur.execute('''INSERT OR REPLACE INTO usda_synonymy
        (accept_id, syn_id) VALUES ( ?, ?)''', 
        ( accept_id, syny_id ) )
    
conn.commit()
print ('Part 2 of plants.py complete. Please review the database ak_usda_plants_db.sqlite for accuracy.')