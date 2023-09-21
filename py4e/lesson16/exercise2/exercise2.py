import sqlite3

connection = sqlite3.connect("exercise2.sqlite")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS Counts")

cursor.execute("""
CREATE TABLE Counts (org TEXT, count INTEGER)""")

filename = input("Enter file name: ")
if len(filename) < 1:
    filename = "mbox.txt"
filehandle = open(filename)
for line in filehandle:
    if line.startswith("From: "):
        pieces = line.split()
        organization = pieces[1].split("@")[1]
        cursor.execute("SELECT count FROM Counts WHERE org = ? ", (organization,))
        row = cursor.fetchone()
        if row is None:
            cursor.execute("""INSERT INTO Counts (org, count)
                    VALUES (?, 1)""", (organization,))
        else:
            cursor.execute("UPDATE Counts SET count = count + 1 WHERE org = ?",
                           (organization,))
connection.commit()

sql = "SELECT org, count FROM Counts ORDER BY count DESC"

for row in cursor.execute(sql):
    print(str(row[0]), row[1])
cursor.close()
