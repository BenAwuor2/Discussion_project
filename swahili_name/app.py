from flask import Flask, render_template,flash
from forms import RegistrationForm, LoginForm

app=Flask(__name__)
app.config['SECRET_KEY'] = "4e6474cd2489a85b59848514ecced2d0"

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

if __name__=='__main__':
    app.run(debug=True)
