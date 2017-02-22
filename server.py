from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import Piece, Composer, connect_to_db, db

from sqlalchemy.orm.exc import NoResultFound

from functions import query_constructor

app = Flask(__name__)

app.secret_key = "secret"

app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():

	return render_template('homepage.html')


@app.route('/search')
def search():

	composers = db.session.query(Composer.composer_id, Composer.name, db.func.count(Piece.composer_id)).group_by(Composer.composer_id, Composer.name).join(Piece).order_by(Composer.name).all()
	periods = db.session.query(Piece.period, db.func.count(Piece.period)).distinct(Piece.period).group_by(Piece.period).order_by(Piece.period).all()
	levels = db.session.query(Piece.level, db.func.count(Piece.level)).distinct(Piece.level).group_by(Piece.level).order_by(Piece.level).all()
	keys = db.session.query(Piece.key, db.func.count(Piece.key)).distinct(Piece.key).group_by(Piece.key).order_by(Piece.key).all()
	tonalities = db.session.query(Piece.tonality, db.func.count(Piece.tonality)).distinct(Piece.tonality).group_by(Piece.tonality).order_by(Piece.tonality).all()

	return render_template('search.html', composers=composers,
										  periods=periods,
										  levels=levels,
										  keys=keys,
										  tonalities=tonalities)

@app.route('/suggest')
def suggest():
	
	pieces = db.session.query(Piece.piece_id, 
							 Piece.title).all()

	composers = db.session.query(Composer.composer_id, Composer.name, db.func.count(Piece.composer_id)).group_by(Composer.composer_id, Composer.name).join(Piece).order_by(Composer.name).all()
	
	return render_template('suggest.html', pieces=pieces, composers=composers)


@app.route('/find-pieces-by-composer')
def get_pieces_by_composer():

	composer_id = request.args.get("composer_id")

	composer = db.session.query(Composer.name).filter_by(composer_id=composer_id).one()[0]
	pieces = db.session.query(Piece).filter_by(composer_id=composer_id).all()

	pieces_arr = [{"composer": composer}]

	for piece in pieces:
		
		pdict = {}

		pdict["piece_id"] = piece.piece_id
		pdict["title"] = piece.title
		
		pieces_arr.append(pdict)

	return jsonify({'pieces_arr': pieces_arr})


@app.route('/suggestion-results')
def suggestion_results():

	piece_id = request.args.get("piece-id")
	piece = db.session.query(Piece).filter_by(piece_id=piece_id).one()

	title = request.args.get("title")
	composer_id = request.args.get("composer")
	period = request.args.get("period")
	level = request.args.get("level")
	key = request.args.get("key")
	tonality = request.args.get("tonality")

	filters = []

	if title:
		title = title
		filters.append('title')
	else: 
		title = ''

	if composer_id:
		composer_id = piece.composer_id
		filters.append('composer')
	else: 
		composer = ''

	if period:
		period = piece.period
		filters.append('period')
	else: 
		period = ''

	if level:
		level = piece.level
		filters.append('level')
	else: 
		level = ''

	if key:
		key = piece.key
		filters.append('key')
	else: 
		key = ''

	if tonality:
		tonality = piece.tonality
		filters.append('tonality')
	else:
		tonality = ''

	pieces = query_constructor(title, composer_id, period, level, key, tonality)

	return render_template('suggestion_results.html', piece=piece,
													  filters=filters,		 
													  pieces=pieces)


@app.route("/results")
def results():

	title = request.args.get("title")
	composer_id = request.args.get("composer_id")
	period = request.args.get("period")
	level = request.args.get("level")
	key = request.args.get("key")
	tonality = request.args.get("tonality")

	pieces = query_constructor(title, composer_id, period, level, key, tonality)

	pieces_arr = []

	for piece in pieces:
		
		pdict = {}
		composer_id = piece.composer_id

		pdict["piece_id"] = piece.piece_id
		pdict["title"] = piece.title
		pdict["composer"] = db.session.query(Composer.name).filter_by(composer_id=composer_id).one()[0]
		pdict["period"] = piece.period
		pdict["level"] = piece.level
		pdict["key"] = piece.key
		pdict["tonality"] = piece.tonality

		pieces_arr.append(pdict)


	return jsonify({'pieces_query_arr': pieces_arr})


##############################################################################

if __name__ == "__main__":

	app.debug = True
	app.jinja_env.auto_reload = app.debug


	connect_to_db(app)

	
	DebugToolbarExtension(app)

	app.run(port=5000, host='0.0.0.0')


