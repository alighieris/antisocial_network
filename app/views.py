from flask import Blueprint, render_template, request, redirect, url_for, send_file
from flask_login import login_required,current_user
from .models import Post, User, File, Profile_pic
from . import db
from io import BytesIO
views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
	posts = db.session.query(Post.id,Post.title,Post.content,Post.date, User.username,User.profile_img_id, Post.image_id).join(User,Post.user_id==User.id).order_by(Post.date)

	return render_template("home.html", user=current_user, posts=posts)



@views.route('/create_post', methods=['GET','POST'])
@login_required
def create_post():
	if request.method == 'POST':
		title = request.form.get('title')
		content = request.form.get('title')
		file = request.files['imageUpload']

		db.session()

		if file.filename == '':
			new_post = Post(title=title,content=content,user_id=current_user.id)
		else:			
			new_file = File(image=file.read(), image_name=file.filename)
			db.session.add(new_file)
			db.session.commit()
			new_post = Post(title=title,content=content,user_id=current_user.id, image_id=new_file.id)

		db.session.add(new_post)
		db.session.commit()

		return redirect(url_for('views.home'))

	return render_template('postar.html', user=current_user)


@views.route('/img/<type>/<img_id>', methods=['GET'])
def img(type,img_id):
	if type == 'profile_img':
		image = Profile_pic.query.filter_by(id=img_id).first()
	elif type == 'post_img':
		image = File.query.filter_by(id=img_id).first()
	else: return

	return send_file(BytesIO(image.image), download_name=image.image_name, as_attachment=True)