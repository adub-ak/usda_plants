# Plants Part 5: Create synonymy table using local plant list

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
DROP TABLE IF EXISTS local_synonymy;

CREATE TABLE local_synonymy (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    code_local TEXT NOT NULL UNIQUE, 
    code_usda TEXT NOT NULL,
    author_usda TEXT,
    usda_status_code TEXT,
    UNIQUE(code_local, code_usda)
);
''')
    
fname = input('Enter the name of local plant list with codes and titles: ')
if len(fname) < 1 : fname = "local_plant_list.txt"
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
    words = line.split(',')
    count = count + 1
    loc_lst = list()
    # this for loop cleans up the double quotes and encodes each element of words to utf-8 and returns a list
    for i in range(len(words)):      
        wrd = words[i].replace('"','')
        encod = wrd.encode('utf-8')
        loc_lst.append(encod)
    #print (lst)
    local_titl = loc_lst[1].decode()
    
    cur.execute('''
    WITH title_count AS (SELECT title, count(title) AS cnt_title FROM 
    (SELECT title FROM usda_accepted WHERE title IS NOT NULL
    UNION ALL
    SELECT syn_title FROM usda_not_accepted WHERE syn_title IS NOT NULL) AS subq
    GROUP BY title
    ORDER BY count(title) DESC),
    spplist AS (SELECT code, title, author, 'accepted' AS usda_status FROM usda_accepted WHERE title IS NOT NULL
    UNION ALL
    SELECT syn_code, syn_title, author, 'not_accepted' AS usda_status FROM usda_not_accepted WHERE syn_title IS NOT NULL)
    SELECT spplist.code, spplist.title, spplist.author, spplist.usda_status, cnt_title FROM spplist
    JOIN title_count
    ON spplist.title = title_count.title
    WHERE spplist.title = ?''', ( local_titl, ) )
    
    test = cur.fetchall()
    #print (loc_lst)
    #print(len(test))
    
    if len(test) == 0:
        print('no match', loc_lst)
        cur.execute('''INSERT OR REPLACE INTO local_synonymy
        (code_local, code_usda, author_usda, usda_status_code) VALUES ( ?, 'n/a', 'no match', 'not recognized' )''', 
        ( loc_lst[0].decode(), ) )
        
        conn.commit()
    
    elif len(test) > 1:
        ti_cnt = 0
        for i in range(len(test)):
            ti_cnt = ti_cnt+1
            print (ti_cnt,':', test[i][2])
        zzz = 0
        while zzz == 0: 
            
            try:
                tnum = input('Matching titles, please enter number of the taxa that matches local list: ')
                if tnum == "done" : break
                tnum_ind = int(tnum)-1
                cur.execute('''INSERT OR REPLACE INTO local_synonymy
                (code_local, code_usda, author_usda, usda_status_code) VALUES ( ?, ?, ?, ?)''', 
                ( loc_lst[0].decode(), test[tnum_ind][0], test[tnum_ind][2], test[tnum_ind][3] ) )
                conn.commit()
                zzz = zzz-1
            
            except KeyboardInterrupt:
                print ('')
                print ('Program interrupted by user...')
                break
            
            except:
                print ('Please enter an integer between 1 and', ti_cnt)
                continue
                
               
    else:
        print(loc_lst)
        cur.execute('''INSERT OR REPLACE INTO local_synonymy
        (code_local, code_usda, author_usda, usda_status_code) VALUES ( ?, ?, ?, ?)''', 
        ( loc_lst[0].decode(), test[0][0], test[0][2], test[0][3] ) )
    
        conn.commit()    

print ('There are', count, 'lines in the local plant list.')
print('This is your local plant list')