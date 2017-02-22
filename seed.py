import requests
from bs4 import BeautifulSoup

from sqlalchemy import func
from model import Piece, Composer

from model import connect_to_db, db
from server import app

import ipdb


def get_data_from_website():
	r = requests.get('http://www.rastallmusic.com/donotdelete/rastall_books2.php?Title=&Composer=&P=&Level=&book=&CD=&PUBLISHER=&PUBNO=&submit=Search%21')
	html = r.text

	soup = BeautifulSoup(html, "html.parser")	
	tables = soup.find_all('table')
	music_table = tables[3]
	rows = music_table.find_all('tr')[1:]

	return rows


def process_composer(row):
	"""Load composers from webpage into database."""

	data = row.find_all('td')
	name = data[2].string

	composer = Composer(name=name)

	return composer


def process_piece(row):
	"""Load pieces from webpage into database."""

	data = row.find_all('td')

	title = data[1].string
	composer_name = data[2].string
	composer_id = db.session.query(Composer.composer_id).filter(Composer.name == composer_name).one()[0]
	period = data[3].string
	level = None
	key = None
	tonality = None

	if data[4].string == 'Prep':
		level = 0;
	elif data[4].string != None:
		level = int(str(data[4].string))

	if ' in ' in title:
		split = title.split(' ')
		string = split[split.index('in') + 1].rstrip(',.:)"')
		lowerstring = string.lower()

		try:
			string_next = split[split.index('in') + 2].rstrip(',.:)"')
		except Exception as e:
			string_next = ''

		if string_next.lower() == 'minor' or string_next.lower() == 'min':
			key = lowerstring
		elif string_next.lower() == 'sharp':
			key = string + '#'
		elif string_next.lower() == 'flat':
			key = string + 'b'
		elif len(string) == 1 and string != ' ':
			key = string
		elif len(string) == 2 and (string[1] == '#' or string[1] == 'b'):
			key = string
		elif len(string) > 2:
			if string[1] == ',':
				key = string[0]
			elif 'sharp' in string:
				key = string[0] + '#'
			elif 'flat' in string:
				key = string[0] + 'b'
		else:
			key = None
	else:
		key = None

	if key != None:
		if key[0].isupper():
			tonality = 'major'
		else:
			tonality = 'minor'

		
	piece = Piece(title=title, composer_id=composer_id, period=period, level=level, key=key, tonality=tonality)

	return piece


def output_data(item): 
	
	db.session.add(item)
	db.session.commit()


################################################################################################

if __name__ == "__main__":
	connect_to_db(app)

	db.create_all()

	website_data = get_data_from_website()
	
	for row in website_data:

		composer = process_composer(row)
		exists = db.session.query(Composer.name).filter(Composer.name == composer.name).scalar()
		if exists is None:
			output_data(composer)

		piece = process_piece(row)
		output_data(piece)

	print "Loaded pieces database."

	
