import json
import sqlite3

connection = sqlite3.connect("rosterdb.sqlite")
cursor = connection.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
""")

filename = input("Enter file name: ")
if len(filename) < 1:
    filename = "roster_data.json"

#   [ "Charley", "si110", 1 ],

str_data = open(filename).read()
json_data = json.loads(str_data)

for entry in json_data:
    name = entry[0]
    title = entry[1]
    role = entry[2]

    cursor.execute("""INSERT OR IGNORE INTO User (name)
        VALUES ( ? )""", (name,))
    cursor.execute("SELECT id FROM User WHERE name = ? ", (name,))
    user_id = cursor.fetchone()[0]

    cursor.execute("""INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )""", (title,))
    cursor.execute("SELECT id FROM Course WHERE title = ? ", (title,))
    course_id = cursor.fetchone()[0]

    cursor.execute("""INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ?)""", (user_id, course_id, role))

    connection.commit()

cursor.execute("""
SELECT 'XYZZY' || hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X LIMIT 1;""")

print(cursor.fetchone())
cursor.close()
