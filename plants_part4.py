# Plants Part 4: Update titles in database in the usda_accepted and usda_not_accepted tables

import sqlite3
import sys
import re

# create database connection to ak_usda_plants_db.sqlite
conn = sqlite3.connect('ak_usda_plants_db.sqlite')
# create database cursor
cur = conn.cursor()

cur.execute('SELECT * FROM usda_titles')
all_titles = cur.fetchall()

for i in all_titles:
    cod = i[1]
    titl = i[2]
    print(cod)
    cur.execute('''UPDATE usda_accepted SET title = ? 
    WHERE code = ?''', ( titl, cod ) )

    cur.execute('''UPDATE usda_not_accepted SET syn_title = ? 
    WHERE syn_code = ?''', ( titl, cod ) )
    
conn.commit()
    
print ('All done for now')