from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required,current_user
from .models import Post, User, File, Profile_pic
from . import db
from .utils import  image2db
from datetime import datetime
import json
views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
	posts = db.session.query(Post.id,Post.title,Post.content,Post.date,User.username,File.image.label('media_img'),Profile_pic.image.label('profile_img')).join(User,Post.user_id==User.id).join(File,Post.image_id==File.id).join(Profile_pic,User.profile_img_id==Profile_pic.id).order_by(Post.date)
	pic = db.session.query(Profile_pic.rendered_image).filter(Profile_pic.id==current_user.profile_img_id).filter(Profile_pic.active==True)
	return render_template("home.html", user=current_user, posts=posts, profile_pic=pic[0].rendered_image)



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
			imageData, rendered_image = image2db(file)
			new_file = File(image=imageData, rendered_image=rendered_image)
			db.session.add(new_file)
			db.session.commit()
			new_post = Post(title=title,content=content,user_id=current_user.id, image_id=new_file.id)

		db.session.add(new_post)
		db.session.commit()

		return redirect(url_for('views.home'))

	return render_template('postar.html', user=current_user)


