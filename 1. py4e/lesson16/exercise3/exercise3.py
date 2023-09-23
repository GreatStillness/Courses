import xml.etree.ElementTree as ET
import sqlite3

connection = sqlite3.connect('exercise3.sqlite')
cursor = connection.cursor()

# Make some fresh tables using executescript()
cursor.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

filename = input('Enter file name: ')
if len(filename) < 1:
    filename = 'Library.xml'


# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
# <key>Genre</key><string>Rock</string>
def lookup(d, key):
    found = False
    for child in d:
        if found:
            return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None


stuff = ET.parse(filename)
tracks = stuff.findall('dict/dict/dict')
print('Dict count:', len(tracks))
for track in tracks:
    if lookup(track, 'Track ID') is None:
        continue

    name = lookup(track, 'Name')
    artist = lookup(track, 'Artist')
    album = lookup(track, 'Album')
    genre = lookup(track, 'Genre')
    count = lookup(track, 'Play Count')
    rating = lookup(track, 'Rating')
    length = lookup(track, 'Total Time')

    if name is None or artist is None or album is None or genre is None:
        continue

    print(name, artist, album, count, rating, length)

    cursor.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', (artist,))
    cursor.execute('SELECT id FROM Artist WHERE name = ? ', (artist,))
    artist_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR IGNORE INTO Genre (name) 
            VALUES ( ? )''', (genre,))
    cursor.execute('SELECT id FROM Genre WHERE name = ? ', (genre,))
    genre_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', (album, artist_id))
    cursor.execute('SELECT id FROM Album WHERE title = ? ', (album,))
    album_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ?, ? )''',
                   (name, album_id, genre_id, length, rating, count))

    connection.commit()
