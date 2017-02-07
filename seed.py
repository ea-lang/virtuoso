import requests
from bs4 import BeautifulSoup

from sqlalchemy import func
from model import Piece

from model import connect_to_db, db
from server import app

r = requests.get('http://www.rastallmusic.com/donotdelete/rastall_books2.php?Title=&Composer=&P=&Level=&book=&CD=&PUBLISHER=&PUBNO=&submit=Search%21')
html = r.text

soup = BeautifulSoup(html, "html.parser")	
tables = soup.find_all('table')
music_table = tables[3]
rows = music_table.find_all('tr')[1:]

def load_pieces():
	"""Load pieces from webpage into database."""

	print "Loading pieces"

	Piece.query.delete() 

	for row in rows:
		data = row.find_all('td')

		title = data[1].string
		composer = data[2].string
		period = data[3].string

		if data[4].string == 'Prep':
			level = 0;
		elif data[4].string != None:
			level = int(str(data[4].string))

		if ' in ' in title:
			split = title.split(' ')
			string = split[split.index('in') + 1].rstrip(',.:)"')
			if len(string) == 1 and string != ' ':
				key = string
			elif len(string) == 2 and (string[1] == '#' or string[1] == 'b'):
				key = string
			elif len(string) > 2:
				if string[1] == ',':
					key = string[0]
				elif 'flat' in string:
					key = string[0] + 'b'
				elif 'sharp' in string:
					key = string[0] + '#'
			else:
				key = None
		else:
			key = None

		piece = Piece(title=title, composer=composer, period=period, level=level, key=key)

		db.session.add(piece)

	db.session.commit()


################################################################################################

if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_pieces()

