import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
#c.execute('DROP TABLE games')
#conn.commit()
#c.execute('''CREATE TABLE games (map, result)''')
c.execute('''DROP TABLE map_notes''')
c.execute('''CREATE TABLE map_notes (
    note_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    map_name VARCHAR(20) NOT NULL,
    note VARCHAR(999) NOT NULL)''')

#for row in c.execute('SELECT * FROM games'):
    #(map, result) = row
    #print(map)
    #print(result)

conn.commit()
conn.close()