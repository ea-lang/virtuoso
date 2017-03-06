from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import Piece, Composer, connect_to_db, db

from sqlalchemy.orm.exc import NoResultFound

from functions import query_constructor, make_piece_dict, make_filter_list, get_pieces, create_radar_dict

app = Flask(__name__)

app.secret_key = "secret"

app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():

	return render_template('homepage.html')


@app.route('/search')
def search():

	composers = db.session.query(Composer.composer_id, Composer.name, db.func.count(Piece.composer_id)).group_by(Composer.composer_id, Composer.name).join(Piece).order_by(Composer.name).all()
	periods = db.session.query(Piece.period, db.func.count(Piece.period)).distinct(Piece.period).filter(Piece.period != None).group_by(Piece.period).order_by(Piece.period).all()
	levels = db.session.query(Piece.level, db.func.count(Piece.level)).distinct(Piece.level).filter(Piece.level != None).group_by(Piece.level).order_by(Piece.level).all()
	keys = db.session.query(Piece.key, db.func.count(Piece.key)).distinct(Piece.key).filter(Piece.key != None).group_by(Piece.key).order_by(Piece.key).all()
	tonalities = db.session.query(Piece.tonality, db.func.count(Piece.tonality)).distinct(Piece.tonality).filter(Piece.tonality != None).group_by(Piece.tonality).order_by(Piece.tonality).all()

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
	pieces = db.session.query(Piece).filter_by(composer_id=composer_id).order_by(Piece.title).all()

	pieces_arr = [{"composer": composer}]

	for piece in pieces:
		
		pdict = {}

		pdict["piece_id"] = piece.piece_id
		pdict["title"] = piece.title
		
		pieces_arr.append(pdict)

	return jsonify({'pieces_arr': pieces_arr})


@app.route('/suggestion-results')
def suggestion_results():

	piece_id = request.args.get("piece_id")
	piece = db.session.query(Piece).filter_by(piece_id=piece_id).one()

	title = ''
	composer_id = piece.composer_id if request.args.get("composer_id") == 'true' else '' 
	period = piece.period if request.args.get("period") == 'true' else ''
	level = piece.level if request.args.get("level") == 'true' else ''
	key = piece.key if request.args.get("key") == 'true' else ''
	tonality = piece.tonality if request.args.get("tonality") == 'true' else ''

	pieces = query_constructor(title, composer_id, period, level, key, tonality)
	pieces_arr = make_piece_dict(pieces)
	my_piece = make_piece_dict([piece])

	filter_list = make_filter_list(composer_id, period, level, key, tonality)

	result_count = 0
	for piece in pieces:
		result_count += 1

	return jsonify({'my_piece': my_piece, 'pieces_query_arr': pieces_arr, 'filters': filter_list, 'count': result_count})


@app.route("/results")
def results():

	title = request.args.get("title")
	composer_id = request.args.get("composer_id")
	period = request.args.get("period")
	level = request.args.get("level")
	key = request.args.get("key")
	tonality = request.args.get("tonality")

	pieces = query_constructor(title, composer_id, period, level, key, tonality)

	pieces_arr = make_piece_dict(pieces)

	result_count = 0
	for piece in pieces:
		result_count += 1


	return jsonify({'pieces_query_arr': pieces_arr, 'count': result_count})


@app.route("/periods-counts.json")
def get_periods_counts():

	periods = db.session.query(Piece.period, db.func.count(Piece.period)).distinct(Piece.period).filter(Piece.period != None).group_by(Piece.period).order_by(Piece.period).all()

	periods_dict = {
                "labels": [],
                "datasets": [
                    {
                        "data": [],
                        "backgroundColor": [
                            "#510b25",
                            "#d1a475",
                            "#0a1754",
                            "#442f13",
                            "#fff5e8",
                            "#f2c4d2"
                        ],
                        "hoverBackgroundColor": [
                            "#510b25",
                            "#d1a475",
                            "#0a1754",
                            "#442f13",
                            "#fff5e8",
                            "#f2c4d2"
                        ]
                    }]
            }

	for period in periods:
		periods_dict["labels"].append(period[0].encode('utf8'))
		periods_dict["datasets"][0]["data"].append(int(str(period[1])))

	return jsonify(periods_dict)


@app.route("/majorkey-counts.json")
def get_majorkeys_counts():

	keys = db.session.query(Piece.key, db.func.count(Piece.key)).distinct(Piece.key).filter(Piece.key != None, Piece.tonality == 'Major').group_by(Piece.key).order_by(Piece.key).all()

	key_dict = {
                "labels": [],
                "datasets": [
                    {
                        "data": [],
                        "backgroundColor": [
                        	"#d1a475",
                        	"#442f13",
                        	"#e51235",
                        	"#ff4967",
                        	"#f2c4d2",
                        	"#b6d0f9",
                        	"#ff6251",
                        	"#510b25",
                        	"#0a1754",
                        	"#fff5e8",
                        	"#fc71b9",
                        	"#f9939d",
                        	"#ffeaf0"
                        ],
                        "hoverBackgroundColor": [
                           	"#d1a475",
                        	"#442f13",
                        	"#e51235",
                        	"#ff4967",
                        	"#f2c4d2",
                        	"#b6d0f9",
                        	"#ff6251",
                        	"#510b25",
                        	"#0a1754",
                        	"#fff5e8",
                        	"#fc71b9",
                        	"#f9939d",
                        	"#ffeaf0"
                        ]
                    }]
            }

	for key in keys:
		key_dict["labels"].append(key[0].encode('utf8'))
		key_dict["datasets"][0]["data"].append(int(str(key[1])))

	return jsonify(key_dict)

@app.route("/minorkey-counts.json")
def get_minorkeys_counts():

	keys = db.session.query(Piece.key, db.func.count(Piece.key)).distinct(Piece.key).filter(Piece.key != None, Piece.tonality == 'Minor').group_by(Piece.key).order_by(Piece.key).all()

	key_dict = {
                "labels": [],
                "datasets": [
                    {
                        "data": [],
                        "backgroundColor": [
                        	"#d1a475",
                        	"#442f13",
                        	"#e51235",
                        	"#ff4967",
                        	"#f2c4d2",
                        	"#b6d0f9",
                        	"#ff6251",
                        	"#510b25",
                        	"#0a1754",
                        	"#fff5e8",
                        	"#fc71b9",
                        	"#f9939d",
                        	"#ffeaf0"
                        ],
                        "hoverBackgroundColor": [
                           	"#d1a475",
                        	"#442f13",
                        	"#e51235",
                        	"#ff4967",
                        	"#f2c4d2",
                        	"#b6d0f9",
                        	"#ff6251",
                        	"#510b25",
                        	"#0a1754",
                        	"#fff5e8",
                        	"#fc71b9",
                        	"#f9939d",
                        	"#ffeaf0"
                        ]
                    }]
            }

	for key in keys:
		key_dict["labels"].append(key[0].encode('utf8'))
		key_dict["datasets"][0]["data"].append(int(str(key[1])))

	return jsonify(key_dict)


@app.route("/level-counts.json")
def get_level_counts():

	levels = db.session.query(Piece.level, db.func.count(Piece.level)).distinct(Piece.level).filter(Piece.level != None).group_by(Piece.level).order_by(Piece.level).all()

	level_dict = {
                "labels": [],
                "datasets": [
                    {
                        "data": [],
                        "backgroundColor": [
                        	"#d1a475",
                        	"#442f13",
                        	"#e51235",
                        	"#ff4967",
                        	"#f2c4d2",
                        	"#b6d0f9",
                        	"#ff6251",
                        	"#510b25",
                        	"#0a1754",
                        	"#fff5e8",
                        	"#fc71b9",
                        	"#f9939d",
                        	"#ffeaf0"
                        ],
                        "hoverBackgroundColor": [
                           	"#d1a475",
                        	"#442f13",
                        	"#e51235",
                        	"#ff4967",
                        	"#f2c4d2",
                        	"#b6d0f9",
                        	"#ff6251",
                        	"#510b25",
                        	"#0a1754",
                        	"#fff5e8",
                        	"#fc71b9",
                        	"#f9939d",
                        	"#ffeaf0"
                        ]
                    }]
            }

	for level in levels:

		if level[0] == 0:
			level_dict["labels"].append('Prep')
		else:
			level_dict["labels"].append(level[0])
		
		level_dict["datasets"][0]["data"].append(int(str(level[1])))

	return jsonify(level_dict)


@app.route("/charts")
def display_charts():

	composers = db.session.query(Composer.composer_id, Composer.name, db.func.count(Piece.composer_id)).having(db.func.count(Piece.composer_id) >= 20).group_by(Composer.composer_id, Composer.name).join(Piece).order_by(Composer.name).all()

	return render_template("charts.html", composers=composers)


@app.route('/radar-charts')
def display_radar_charts():

	composers = db.session.query(Composer.composer_id, Composer.name, db.func.count(Piece.composer_id)).having(db.func.count(Piece.composer_id) >= 20).group_by(Composer.composer_id, Composer.name).join(Piece).order_by(Composer.name).all()
	periods = db.session.query(Piece.period, db.func.count(Piece.period)).distinct(Piece.period).having(db.func.count(Piece.period) > 1).filter(Piece.period != None).group_by(Piece.period).order_by(Piece.period).all()

	return render_template("radar-charts.html", composers=composers, periods=periods)


@app.route("/radar-chart.json")
def create_radar_chart_data():

	if request.args.get('all') != None:
		tonality = request.args.get('all')
		data = get_pieces('all', '', '', tonality)
		radar_dict = create_radar_dict(data)
	else:
		category = request.args.get('category')
		filter_1 = request.args.get('filter1')
		filter_2 = request.args.get('filter2')
		tonality = request.args.get('tonality')

		data = get_pieces(category, filter_1, filter_2, tonality)
		radar_dict = create_radar_dict(data)

	return jsonify(radar_dict)


@app.route("/render-menus.json")
def render_menus():

	category = request.args.get("category")

	options_dict = {"options": [], "category": category}

	if category == "all":
		options_dict = {}
	else:
		if category == "composer": 
			options = db.session.query(Composer.composer_id, Composer.name, db.func.count(Piece.composer_id).filter(Piece.key != None)).having(db.func.count(Piece.composer_id) >= 3).group_by(Composer.composer_id, Composer.name).join(Piece).order_by(Composer.name).all()
		if category == "period":
			options = db.session.query(Piece.period, db.func.count(Piece.period).filter(Piece.key != None)).distinct(Piece.period).having(db.func.count(Piece.period) > 20).filter(Piece.period != None).group_by(Piece.period).order_by(Piece.period).all()
		if category == "level":
			options = db.session.query(Piece.level, db.func.count(Piece.level).filter(Piece.key != None)).distinct(Piece.level).filter(Piece.level != None).group_by(Piece.level).order_by(Piece.level).all()

		if category == "composer":
			for option in options:
				if option[2] > 5:
					options_dict["options"].append({"composer_id": option[0], "name": option[1], "piece_count": option[2]})
		else:
			for option in options:
				options_dict["options"].append({"option": option[0], "piece_count": option[1]})

	return jsonify(options_dict)

##############################################################################

if __name__ == "__main__":

	app.debug = True
	app.jinja_env.auto_reload = app.debug


	connect_to_db(app)

	
	DebugToolbarExtension(app)

	app.run(port=5000, host='0.0.0.0')


