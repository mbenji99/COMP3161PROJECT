import os
from flask import Flask
from flask_login import LoginManager
from flask import render_template, request, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from forms import LecturerRegistrationForm, LoginForm, StudentRegistrationForm, RegistrationForm, CourseRegistration

app = Flask(__name__)
app.secret_key = 'something'

login_manager = LoginManager()
login_manager.init_app(app) 
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return current_user.get(user_id)


@app.route('/',methods=['GET'])
def index():
    return render_template('login.html')

app.run()

