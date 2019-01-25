from flask import Blueprint, session, render_template, url_for, flash,redirect, request,abort, jsonify, make_response
from settings import PROTECTED_FOLDER
import uuid
import bcrypt
from flask_mail import Message
from flask_login import login_user, current_user, login_required, logout_user
from datetime import timedelta

from user.forms import RegisterForm, LoginForm, ForgotForm, PasswordBaseForm
from user.models import User
from home.forms import home_form
from flask import current_app
from application import mail, login_manager 
#import mail

user_app = Blueprint('user_app', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id = user_id)

@user_app.route('/register/', methods=('GET', 'POST'))
def register():
	if request.method == "POST":
		flag = 1
	else:
		flag = 0
	if current_user.is_authenticated:
	    print("Da log in roi ")
	    return redirect(url_for("home_app.home"))
	form = home_form()
	register_form = RegisterForm()

	if register_form.validate_on_submit():
		print("=======> ok ")
		salt = bcrypt.gensalt()
		hashed_password = bcrypt.hashpw(register_form.password.data.encode("utf-8"), salt)
		code = str(uuid.uuid4())
		user = User(
            username=register_form.username.data,
            password=hashed_password,
            email=register_form.email.data,
            first_name=register_form.first_name.data,
            last_name=register_form.last_name.data,
            change_configuration={
                "new_email": register_form.email.data.lower(),
                "confirmation_code": code
                }
            )
		body_html = render_template('mail/user/register.html', user=user)
		body_text = render_template('mail/user/register.txt', user=user)
		msg = Message("Wellcome to Whatever.vn",
                  sender="lamduyuit@gmail.com",
                  recipients=[user.email])
		msg.text = body_text
		msg.html = body_html
		resp = mail.send(msg)
		user.save()
		flash("Successful account creation ! You need to activate by clicking on the link sent to the email")
		#print(user._data)
	else:
		print(register_form.errors.keys())
		for i,val in register_form.errors.items():
			print(i, " || ", val)

	print(register_form.errors.keys())
	print(flag) 
	return render_template("user/register.html", form = form,error=None, register_form = register_form, flag = flag)

@user_app.route('/confirm/<username>/<code>', methods=('GET', 'POST'))
def confirm(username, code):
    user = User.objects.filter(username=username).first()
    if user and user.change_configuration and user.change_configuration.get('confirmation_code'):
        if code == user.change_configuration.get('confirmation_code'):
            user.email = user.change_configuration.get('new_email')
            user.change_configuration = {}
            user.email_confirmed = True
            user.save()
            flash("The account has been successfully activated !")
            return redirect(url_for("home_app.home"))
    else:
        abort(404)

@user_app.route('/login/', methods=('GET', 'POST'))
def login():
	if request.method == "POST":
	    flag = 1
	else:
	    flag = 0
	print(session)
	if current_user.is_authenticated:
	    print("Da log in roi ")
	    return redirect(url_for("home_app.home"))
	else:
	    form = home_form()
	    login_form = LoginForm()
	    error = None
	    
	    if request.method == 'GET' and request.args.get('next'):
	        session['next'] = request.args.get('next')
	        
	    if login_form.validate_on_submit():
	        user = User.objects.filter(
	            username=login_form.username.data
	            ).first()
	        if user:
	            if user.email_confirmed == False:
	                flash(" Vui lòng kích hoạt tài khoản qua email !")
	                flag = 0
	                return render_template("user/login.html", form = form,error=error, login_form = login_form, flag = flag)
	            if bcrypt.hashpw(login_form.password.data.encode("utf-8"), user.password.encode("utf-8")) == user.password.encode("utf-8"):
	                login_user(user, remember = True, duration = timedelta(days=60))
	                flash("Login successfully !")
	                #session['username'] = login_form.username.data
	                """
	                if 'next' in session:
	                    next = session.get('next')
	                    session.pop('next')
	                    
	                    if not is_safe_url(next):
	                        return abort(400)
	                    
	                    return redirect(next)
	                else:
	                """
	                return redirect(url_for("home_app.valuation"))
	            else:
	                print("Khong dung mat khau")
	                user = None
	        if not user:
	            error = 'Incorrect credentials !'
	    else:
	    	#error = ""
	    	for i,val in login_form.errors.items():
	    		print(i, " || ", val)
	    return render_template("user/login.html", form = form,error=error, login_form = login_form, flag = flag)
@user_app.route('/logout/', methods=('GET', 'POST'))
@login_required
def logout():
	logout_user()
	return redirect(url_for("user_app.login"))

@user_app.route('/forgot/', methods=('GET', 'POST'))
def forgot():
    if request.method == "POST":
        flag = 1
    else:
        flag = 0
    error = None
    form = home_form()
    forgot_form = ForgotForm()
    if forgot_form.validate_on_submit():
        user = User.objects.filter(email=forgot_form.email.data.lower()).first()
        if user:
            code = str(uuid.uuid4())
            user.change_configuration={
                "password_reset_code": code
            }
            user.save()
            
            # email the user
            body_html = render_template('mail/user/password_reset.html', user=user)
            body_text = render_template('mail/user/password_reset.txt', user=user)
            msg = Message("Password reset request",
                  sender="lamduyuit@gmail.com",
                  recipients=[user.email])
            msg.text = body_text
            msg.html = body_html
            resp = mail.send(msg)
            
        flash("You will receive a password reset email if we find that email in our system")
    print(forgot_form.errors)
    return render_template("user/forgot.html", form = form, error = error, forgot_form = forgot_form, flag = flag)

@user_app.route('/password_reset/<username>/<code>', methods=('GET', 'POST'))
def password_reset(username, code):
    if request.method == "POST":
        flag = 1
    else:
        flag = 0
    user = User.objects.filter(username=username).first()
    #user.change_configuration = {"password_reset_code": code}
    #user.save()
    if not user or code != user.change_configuration.get('password_reset_code'):
        abort(404)
    password_reset_form = PasswordBaseForm()
    form = home_form()
    if password_reset_form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_reset_form.password.data.encode("utf-8"), salt)
        print(hashed_password, type(hashed_password))
        user.password = hashed_password.decode("utf-8")
        user.change_configuration = {}
        user.save()
        flash("Password reset successfully !")
        #return redirect(url_for("home_app.valuation"))
    return render_template("user/password_reset.html", form = form, error = None, password_reset_form = password_reset_form, flag = flag, username = username, code = code)