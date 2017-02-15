from seed import process_piece
from bs4 import BeautifulSoup


def test_major_key():
	html = '<tr><td>135</td><td>Musette in D, BWV 126</td><td>Bach, J.S.</td><td>Baroque</td><td>4</td><td>Joy of First Classics</td><td>no</td><td>Yorktown</td><td>YK21736</td></tr>'
	soup = BeautifulSoup(html, "html.parser")
	piece = process_piece(soup)
	assert piece.key == 'D'


def test_key_at_end():
	html = '<tr><td>136</td><td>Minuet in F</td><td>Mozart, L.</td><td>Classical</td><td>4</td><td>Joy of First Classics</td><td>no</td><td>Yorktown</td><td>YK21736</td></tr>'
	soup = BeautifulSoup(html, "html.parser")
	piece = process_piece(soup)
	assert piece.key == 'F'

def test():
	html = '<tr><td>190</td><td>Duet in Contrary Motion</td><td>Reichardt</td><td>Classical</td><td>2</td><td>Joy of First Classics, bk. 2</td><td>no</td><td>Yorktown</td><td>YK 20568</td></tr>'
	soup = BeautifulSoup(html, "html.parser")
	piece = process_piece(soup)
	assert piece.key == None