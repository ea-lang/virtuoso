from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import Piece, connect_to_db, db

from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)

app.secret_key = "secret"

app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():

	return render_template('homepage.html')


@app.route('/search')
def search():

	composers = db.session.query(Piece.composer).distinct(Piece.composer).all()
	periods = db.session.query(Piece.period).distinct(Piece.period).all()
	levels = db.session.query(Piece.level).distinct(Piece.level).all()
	keys = db.session.query(Piece.key).distinct(Piece.key).all()

	return render_template('search.html', composers=composers,
											periods=periods,
											levels=levels,
											keys=keys)


@app.route("/results")
def results():

	title = request.args.get("title")
	composer = request.args.get("composer")
	period = request.args.get("period")
	level = request.args.get("level")
	key = request.args.get("key")

	def query_constructor(title='', composer='', period='', level='', key=''):

		pieces_query = db.session.query(Piece.piece_id, 
						 Piece.title,
						 Piece.composer, 
						 Piece.period,
						 Piece.level,
						 Piece.key)

		if title != '':
			pieces_query = pieces_query.filter(Piece.title.like("%" + title + "%"))

		if composer != '':
			pieces_query = pieces_query.filter(Piece.composer == composer)

		if period != '':
			pieces_query = pieces_query.filter(Piece.period == period)

		if level != '':
			pieces_query = pieces_query.filter(Piece.level == int(level))

		if key != '':
			pieces_query = pieces_query.filter(Piece.key == key)	

		results = pieces_query.all()

		return results

	results = query_constructor(title, composer, period, level, key)

	return render_template('results.html', results=results)


##############################################################################

if __name__ == "__main__":

	app.debug = True
	app.jinja_env.auto_reload = app.debug


	connect_to_db(app)

	
	DebugToolbarExtension(app)

	app.run(port=5000, host='0.0.0.0')


