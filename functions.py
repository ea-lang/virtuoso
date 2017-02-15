from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import Piece, connect_to_db, db

from sqlalchemy.orm.exc import NoResultFound


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