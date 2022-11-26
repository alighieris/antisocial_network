from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id',db.Integer, db.ForeignKey('user.id')))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(32), unique=True)
	username = db.Column(db.String(16), unique=True)
	password = db.Column(db.String(64))
	first_name = db.Column(db.String(32))
	register_date = db.Column(db.DateTime(timezone=True), default=func.now())
	profile_img_id = db.Column(db.Integer, db.ForeignKey('profile_pic.id'))
	post = db.relationship('Post') # em relationship precisa ser capitalizado igual ao nome da classe
	
	''' Essa relação liga User a outro(s) User.
		A relação definida aqui é "followed", ou seja, esse campo do db vai retornar à direita os 
		Users que o User à esquerda segue.

		Os parâmetros são:
		'User' - a entidade direita da relação
		secondary - a tabela de associação utilizada
		primaryjoin - indica a condição que liga o User à esquerda (follower) ao User à direita (followed)
		secondaryjoin - indica a condição que liga o User à direita (followed) ao User à esquerda (follower)
		backref - define como a relação será acessada a partir da entidade do lado direito, a partir da esquerda
				a relação é nomeada "followed", então a partir do lado direito, será nomeada "followers".
				O parâmetro 'lazy' indica o modo de execução da query. O modo 'dynamic' faz com que a query
				não rode até que seja explicitamente solicitada, nesse caso aplicado ao lado direito.
		lazy - similar ao definido dentro do 'backref', mas se aplicando ao lado esquerdo, ao invés do direito
	'''
	followed = db.relationship(
		'User', secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref = db.backref('followers', lazy = 'dynamic'), lazy='dynamic'
	)

	def followed_posts(self):
		''' Retorna a lista dos posts de usuários seguidos.
		Faz join dos posts com a tabela auxiliar de followers, trazendo os ids de todos os seguidores
		do usuário de determinado post. Filtra apenas os posts seguidos pelo usuário ativo (self).
		Depois faz union com os próprios posts e ordena por data.
		'''
		followed = Post.query.join(followers,(followers.c.followed_id == Post.user_id)
		).filter(followers.c.follower_id == self.id)
		own = Post.query.filter_by(Post.user_id == self.id)
		return followed.union(own).order_by(Post.date.desc())

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
	image_name = db.Column(db.Text, nullable=False)
	post = db.relationship('Post')

class Profile_pic(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime(timezone=True), default=func.now())
	image = db.Column(db.LargeBinary, nullable=False)
	image_name = db.Column(db.Text, nullable=False)
	active = db.Column(db.Boolean)
	user = db.relationship('User')