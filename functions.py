from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import Piece, Composer, connect_to_db, db

from sqlalchemy.orm.exc import NoResultFound


def query_constructor(title, composer_id, period, level, key, tonality):

	pieces_query = db.session.query(Piece)

	if title != '' and title is not None:
		pieces_query = pieces_query.filter(Piece.title.ilike("%" + title + "%"))

	if composer_id != '' and composer_id is not None:
		pieces_query = pieces_query.filter(Piece.composer_id == composer_id)

	if period != '' and period is not None:
		pieces_query = pieces_query.filter(Piece.period == period)

	if level != '' and level is not None:
		pieces_query = pieces_query.filter(Piece.level == int(level))

	if key != '':
		pieces_query = pieces_query.filter(Piece.key == key)	

	if tonality != '':
		pieces_query = pieces_query.filter(Piece.tonality == tonality)	

	results = pieces_query.all()

	return results


def make_piece_dict(pieces):

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

	return pieces_arr


def make_filter_list(composer_id, period, level, key, tonality):

	filters = []

	if composer_id != '':
		filters.append('composer')

	if period != '':
		filters.append('period')

	if level != '':
		filters.append('level')

	if key != '':
		filters.append('key')

	if tonality != '':
		filters.append('tonality')

	return filters


def get_pieces(category, filter_1, filter_2, tonality):
	
	data = {'category': category, 
			'pieces_1': None, 
			'pieces_2': None, 
			'tonality': tonality, 
			'label_1': None, 
			'label_2': None,
			'all': None }

	if category == 'all':
		data['pieces_2'] = db.session.query(Piece).filter_by(tonality=tonality).all()
		data['all'] = True
		return data

	if category == 'composer':
		if filter_1 != None and filter_1 != '':
			data['pieces_1'] = db.session.query(Piece).filter_by(composer_id=int(str(filter_1)), tonality=tonality).all()
			data['label_1'] = db.session.query(Composer.name).filter_by(composer_id=int(str(filter_1))).one()[0]
		if filter_2 != None and filter_2 != '':
			data['pieces_2'] = db.session.query(Piece).filter_by(composer_id=int(str(filter_2)), tonality=tonality).all()
			data['label_2'] = db.session.query(Composer.name).filter_by(composer_id=int(str(filter_2))).one()[0]
		return data

	if category == 'period':
		if filter_1 != None and filter_1 != '':
			data['pieces_1'] = db.session.query(Piece).filter_by(period=filter_1, tonality=tonality).all()
			data['label_1'] = filter_1	
		if filter_2 != None and filter_2 != '':
			data['pieces_2'] = db.session.query(Piece).filter_by(period=filter_2, tonality=tonality).all()	
		return data

	if category == 'level':
		if filter_1 != None and filter_1 != '':
			data['pieces_1'] = db.session.query(Piece).filter_by(level=int(str(filter_1)), tonality=tonality).all()	
		if filter_2 != None and filter_2 != '':
			data['pieces_2'] = db.session.query(Piece).filter_by(level=int(str(filter_2)), tonality=tonality).all()	
		return data


def create_radar_dict(pieces):

	data = {
    		"labels": [],
    		"datasets": [
        	{
	            "label": "None",
	            "backgroundColor": "rgba(88,146,227,0.2)",
	            "borderColor": "rgba(88,146,227,1)",
	            "pointBackgroundColor": "rgba(88,146,227,1)",
	            "pointBorderColor": "#fff",
	            "pointHoverBackgroundColor": "#fff",
	            "pointHoverBorderColor": "rgba(88,146,227,1)",
	            "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        	},
        	{
	            "label": "None",
	            "backgroundColor": "rgba(255,99,132,0.2)",
	            "borderColor": "rgba(255,99,132,1)",
	            "pointBackgroundColor": "rgba(255,99,132,1)",
	            "pointBorderColor": "#fff",
	            "pointHoverBackgroundColor": "#fff",
	            "pointHoverBorderColor": "rgba(255,99,132,1)",
	            "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        	}
    	]
	}

	if pieces['tonality'] == 'Major':

		data["labels"] = ["C", "G", "D", "A", "E", "B", "Gb/F#", "Db", "Ab", "Eb", "Bb", "F"]

		if pieces['pieces_1'] != None:

			for piece in pieces['pieces_1']:

				if pieces['category'] == 'composer':
					data["datasets"][0]["label"] = piece.composer.name.encode('utf8')
				elif pieces['category'] == 'period':
					data["datasets"][0]["label"] = piece.period.encode('utf8')
				elif pieces['category'] == 'level':
					data["datasets"][0]["label"] = piece.level

				if piece.key == "Gb" or piece.key == "F#":
					data["datasets"][0]["data"][6] += 1
				else:
					data["datasets"][0]["data"][data["labels"].index(piece.key)] += 1

		if pieces['pieces_2'] != None:

			for piece in pieces['pieces_2']:

				if pieces['category'] == 'composer':
					data["datasets"][1]["label"] = piece.composer.name.encode('utf8')
				elif pieces['category'] == 'period':
					data["datasets"][1]["label"] = piece.period.encode('utf8')
				elif pieces['category'] == 'level':
					data["datasets"][1]["label"] = piece.level

				if piece.key == "Gb" or piece.key == "F#":
					data["datasets"][1]["data"][6] += 1
				else:
					data["datasets"][1]["data"][data["labels"].index(piece.key)] += 1


	if pieces['tonality'] == 'Minor':

		data['labels'] = ["a", "e", "b", "f#", "c#", "g#/ab", "d#/eb", "bb/a#", "f", "c", "g", "d"]

		if pieces['pieces_1'] != None:

			for piece in pieces['pieces_1']:

				if pieces['category'] == 'composer':
					data["datasets"][0]["label"] = piece.composer.name.encode('utf8')
				elif pieces['category'] == 'period':
					data["datasets"][0]["label"] = piece.period.encode('utf8')
				elif pieces['category'] == 'level':
					data["datasets"][0]["label"] = piece.level

				if piece.key == "g#" or piece.key == "ab":
					data["datasets"][0]["data"][5] += 1
				elif piece.key == 'd#' or piece.key == 'eb':
					data["datasets"][0]["data"][6] += 1
				elif piece.key == 'bb' or piece.key == 'a#':
					data["datasets"][0]["data"][7] += 1
				else:
					data["datasets"][0]["data"][data["labels"].index(piece.key)] += 1

		if pieces['pieces_2'] != None:

			for piece in pieces['pieces_2']:

				if pieces['category'] == 'composer':
					data["datasets"][1]["label"] = piece.composer.name.encode('utf8')
				elif pieces['category'] == 'period':
					data["datasets"][1]["label"] = piece.period.encode('utf8')
				elif pieces['category'] == 'level':
					data["datasets"][1]["label"] = piece.level

				if piece.key == "g#" or piece.key == "ab":
					data["datasets"][1]["data"][5] += 1
				elif piece.key == 'd#' or piece.key == 'eb':
					data["datasets"][1]["data"][6] += 1
				elif piece.key == 'bb' or piece.key == 'a#':
					data["datasets"][1]["data"][7] += 1
				else:
					data["datasets"][1]["data"][data["labels"].index(piece.key)] += 1

	if pieces['all']:
		del data["datasets"][0]
		data["datasets"][0]["label"] = "All Pieces"


	return data

		

		


