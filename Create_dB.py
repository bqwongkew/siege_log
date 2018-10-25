import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
#c.execute('DROP TABLE games')
#conn.commit()
c.execute('''CREATE TABLE games (map, result)''')
# c.execute("INSERT INTO games VALUES ('kafe', 'won')")
for row in c.execute('SELECT * FROM games'):
    (map, result) = row
    print(map)
    print(result)


conn.commit()

conn.close()