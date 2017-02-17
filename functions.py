from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import Piece, connect_to_db, db

from sqlalchemy.orm.exc import NoResultFound


def query_constructor(title, composer, period, level, key, tonality):

	pieces_query = db.session.query(Piece.piece_id, 
					 Piece.title,
					 Piece.composer, 
					 Piece.period,
					 Piece.level,
					 Piece.key,
					 Piece.tonality)

	if title != '' and title is not None:
		pieces_query = pieces_query.filter(Piece.title.ilike("%" + title + "%"))

	if composer != '' and composer is not None:
		pieces_query = pieces_query.filter(Piece.composer == composer)

	if period != '' and period is not None:
		pieces_query = pieces_query.filter(Piece.period == period)

	if level != '' and level is not None:
		pieces_query = pieces_query.filter(Piece.level == int(level))

	if key != '' and key is not None:
		pieces_query = pieces_query.filter(Piece.key == key)	

	if tonality != '' and tonality is not None:
		pieces_query = pieces_query.filter(Piece.tonality == tonality)	

	results = pieces_query.all()

	# print title, composer, period, level, key
	return results