from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import Piece, connect_to_db, db

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

	composers = db.session.query(Piece.composer, db.func.count(Piece.composer)).distinct(Piece.composer).group_by(Piece.composer).order_by(Piece.composer).all()
	periods = db.session.query(Piece.period, db.func.count(Piece.period)).distinct(Piece.period).group_by(Piece.period).order_by(Piece.period).all()
	levels = db.session.query(Piece.level, db.func.count(Piece.level)).distinct(Piece.level).group_by(Piece.level).order_by(Piece.level).all()
	keys = db.session.query(Piece.key, db.func.count(Piece.key)).distinct(Piece.key).group_by(Piece.key).order_by(Piece.key).all()

	return render_template('search.html', composers=composers,
											periods=periods,
											levels=levels,
											keys=keys)

@app.route('/suggest')
def suggest():
	
	pieces = db.session.query(Piece.piece_id, 
							 Piece.title).all()

	composers = db.session.query(Piece.composer, db.func.count(Piece.composer)).distinct(Piece.composer).group_by(Piece.composer).order_by(Piece.composer).all()

	return render_template('suggest.html', pieces=pieces, composers=composers)


@app.route('/find-pieces-by-composer')
def get_pieces_by_composer():

	composer = request.args.get("composer")
	pieces = db.session.query(Piece.piece_id, Piece.title).filter_by(composer=composer).all()

	return render_template("findpiecesbycomposer.html", composer=composer, pieces=pieces)


@app.route('/suggestion-results')
def suggestion_results():

	piece_id = request.args.get("piece")
	piece = db.session.query(Piece).filter_by(piece_id=piece_id).one()

	title = request.args.get("title")
	composer = request.args.get("composer")
	period = request.args.get("period")
	level = request.args.get("level")
	key = request.args.get("key")

	filters = []

	if title:
		title = title
		filters.append('title')
	else: 
		title = ''

	if composer:
		composer = piece.composer
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

	results = query_constructor(title, composer, period, level, key)

	return render_template('suggestion_results.html', piece=piece, 
													  results=results,
													  filters=filters)


@app.route("/results")
def results():

	title = request.args.get("title")
	composer = request.args.get("composer")
	period = request.args.get("period")
	level = request.args.get("level")
	key = request.args.get("key")

	query = query_constructor(title, composer, period, level, key)

	return jsonify({'pieces_query_arr': query})


##############################################################################

if __name__ == "__main__":

	app.debug = True
	app.jinja_env.auto_reload = app.debug


	connect_to_db(app)

	
	DebugToolbarExtension(app)

	app.run(port=5000, host='0.0.0.0')


