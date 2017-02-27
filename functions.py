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


