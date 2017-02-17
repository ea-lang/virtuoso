from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Piece(db.Model):

	__tablename__ = "pieces"

	piece_id = db.Column(db.Integer, 
				   primary_key=True,
				   autoincrement=True)
	title = db.Column(db.String(100), nullable=False, unique=False)
	composer = db.Column(db.String(50), nullable=True, unique=False)
	period = db.Column(db.String(50), nullable=True, unique=False)
	level = db.Column(db.Integer, nullable=True, unique=False)
	key = db.Column(db.String(50), nullable=True, unique=False)
	tonality = db.Column(db.String(50), nullable=True, unique=False)

	def __repr__(self):

		return "<Piece piece_id=%d title=%s composer=%s>" % (self.piece_id, self.title, self.composer) 

######################################################################################

def connect_to_db(app):

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pieces'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."