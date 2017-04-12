import xml.etree.ElementTree as ET
import urllib
import psycopg2
import psycopg2.extras
import os

try:
    conn = psycopg2.connect("dbname='1720465_Thiago' user='m0n0p0ly' host='200.134.10.32' password='#n0m0n3y#'")
except:
    print "I am unable to connect to the database."

cur = conn.cursor()

person_tree = ET.parse(urllib.urlopen('http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/person.xml'))
music_tree = ET.parse(urllib.urlopen('http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/music.xml'))
movie_tree = ET.parse(urllib.urlopen('http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/movie.xml'))
knows_tree = ET.parse(urllib.urlopen('http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/knows.xml'))

person_root = person_tree.getroot()
music_root = music_tree.getroot()
movie_root = movie_tree.getroot()
knows_root = knows_tree.getroot()

#Poe pessoa na tabela
for person in person_root:
    cur.execute("SELECT login FROM pessoa WHERE login = '%s'" % (person.get('uri')))
    if cur.rowcount <= 0:
    	cur.execute("INSERT INTO pessoa VALUES ('%s','%s','%s')" % (person.get('hometown'), person.get('name'), person.get('uri')))
    conn.commit()

for music in music_root:
    #Poe musica na tabela
    cur.execute("SELECT id FROM ArtistaMusical WHERE id = '%s'" % (music.get('bandUri')))
    if cur.rowcount <= 0:  	
	cur.execute("INSERT INTO ArtistaMusical(id) VALUES ('%s')" % (music.get('bandUri')))
    #Preenche CurteMusica
    cur.execute("SELECT C.curtidor, C.artista, C.rating FROM curtemusica as C WHERE C.curtidor = '%s' AND C.artista = '%s' AND C.rating = '%s'" % (music.get('person'), music.get('bandUri'), music.get('rating')))
    if cur.rowcount <= 0:
	cur.execute("INSERT INTO CurteMusica VALUES ('%s','%s','%s')" % (music.get('person'), music.get('bandUri'), music.get('rating')))
    conn.commit()

for movie in movie_root:
    #Poe filme na tabela
    cur.execute("SELECT id FROM Filme WHERE id = '%s'" % (movie.get('movieUri')))
    if cur.rowcount <= 0:
	cur.execute("INSERT INTO Filme(id) VALUES ('%s')" % (movie.get('movieUri')))
    #Preenche CurteFilme
    cur.execute("SELECT C.curtidor, C.filme, C.rating FROM curtefilme as C WHERE C.curtidor = '%s' AND C.filme = '%s' AND C.rating = '%s'" % (movie.get('person'), movie.get('movieUri'), movie.get('rating')))
    if cur.rowcount <= 0:
        cur.execute("INSERT INTO CurteFilme VALUES ('%s','%s','%s')" % (movie.get('person'), movie.get('movieUri'), movie.get('rating')))
    conn.commit()

#Preenche tabela de conhecidos (Registra)
for knows in knows_root:
    cur.execute("SELECT login_registrador, login_registrado FROM Registra WHERE login_registrador = '%s'AND login_registrado = '%s' " % (knows.get('person'), knows.get('colleague')))
    if cur.rowcount <= 0:
        cur.execute("INSERT INTO Registra VALUES ('%s', '%s')" % (knows.get('person'), knows.get('colleague')))
    conn.commit()

