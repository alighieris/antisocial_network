from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Profile_pic
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from datetime import datetime
from .utils import image2db
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		user = User.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password, password):
				flash('Login com sucesso!', category='sucess')
				login_user(user, remember=True)
				return redirect(url_for('views.home'))
			else:
				flash('Login deu errado, boa sorte tentando lembrar a senha.', category='error')
		else:
			flash('Esse email não existe.', category='error')
	return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
	print(request.method)
	if request.method == 'POST':
		email = request.form.get('email')
		username = request.form.get('username')
		firstName = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
		file = request.files['imageUpload']



		user = User.query.filter_by(email=email).first()
		if user:
			flash('Esse email já existe', category='error')
		elif len(email) < 5:
			flash('Email deve ter mais de 3 caracteres.', category='error')
		elif len(firstName) < 2:
			flash('Isso não é nome de gente...', category='error')
		elif password1 != password2:
			flash('Errooou a confirmação de senha.', category='error')
		else:
			flash('Conta criada com sucesso!', category='sucess')

			imageData, rendered_image = image2db(file)
			new_file = Profile_pic(image=imageData, rendered_image=rendered_image,active=True)
			db.session.add(new_file)
			db.session.commit()

			new_user = User(
				email=email, first_name=firstName, username=username, 
				password=generate_password_hash(password1, method='sha256'), profile_img_id=new_file.id)
			db.session.add(new_user)
			db.session.commit()

			login_user(new_user, remember=True)
			return redirect(url_for('views.home'))
	return render_template("sign_up.html", user=current_user)