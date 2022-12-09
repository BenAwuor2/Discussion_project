from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app=Flask(__name__)
app.config['SECRET_KEY'] = "4e6474cd2489a85b59848514ecced2d0"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/Dinah twirie/Desktop/Alx_projects/Discussion_project/swahili_name/databs.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/home')
def home():
    
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email= form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created!</h1>'
        
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(username=form.username.data).first()
        if user:  
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1>Invalid username or password</h1>'
    
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', name = current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
if __name__=='__main__':
    app.run(debug=True)