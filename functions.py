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

	if key != '' and key is not None:
		pieces_query = pieces_query.filter(Piece.key == key)	

	if tonality != '' and tonality is not None:
		pieces_query = pieces_query.filter(Piece.tonality == tonality)	

	results = pieces_query.all()

	return results