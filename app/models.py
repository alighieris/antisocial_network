from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(32), unique=True)
	username = db.Column(db.String(16), unique=True)
	password = db.Column(db.String(64))
	first_name = db.Column(db.String(32))
	register_date = db.Column(db.DateTime(timezone=True), default=func.now())
	profile_img_id = db.Column(db.Integer, db.ForeignKey('profile_pic.id'))
	post = db.relationship('Post') # em relationship precisa ser capitalizado igual ao nome da classe

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	content = db.Column(db.String(256))
	date = db.Column(db.DateTime(timezone=True), default=func.now())
	up = db.Column(db.Integer)
	down = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # ao definir a foreign key precisa ser tudo minusculo
	image_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=True)

class File(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime(timezone=True), default=func.now())
	image = db.Column(db.LargeBinary, nullable=False)
	rendered_image = db.Column(db.Text, nullable=False)
	post = db.relationship('Post')

class Profile_pic(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime(timezone=True), default=func.now())
	image = db.Column(db.LargeBinary, nullable=False)
	rendered_image = db.Column(db.Text, nullable=False)
	active = db.Column(db.Boolean)
	user = db.relationship('User')