# app.py

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo

# Initialize the app and configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'sponsor', 'influencer'
    # Additional fields for different roles

    # Sponsor fields
    company_name = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    budget = db.Column(db.Integer)
    # Influencer fields
    category = db.Column(db.String(100))
    niche = db.Column(db.String(100))
    reach = db.Column(db.Integer)

    def __repr__(self):
        return f'<User {self.username}>'

# Define Campaign model
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    start_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    end_date = db.Column(db.DateTime)
    budget = db.Column(db.Integer)
    visibility = db.Column(db.String(10))  # 'public' or 'private'
    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Campaign {self.name}>'

# Define AdRequest model
class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    messages = db.Column(db.Text)
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Integer)
    status = db.Column(db.String(10), default='Pending')  # 'Pending', 'Accepted', 'Rejected'

    def __repr__(self):
        return f'<AdRequest {self.id}>'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=200)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('sponsor', 'Sponsor'), ('influencer', 'Influencer')], validators=[DataRequired()])
    submit = SubmitField('Register')

# Define Routes
@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/')
# def index():
#     if current_user.is_authenticated:
#         if current_user.role == 'admin':
#             return redirect(url_for('admin_dashboard'))
#         elif current_user.role == 'sponsor':
#             return redirect(url_for('sponsor_dashboard'))
#         elif current_user.role == 'influencer':
#             return redirect(url_for('influencer_dashboard'))
#     return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'sponsor':
                return redirect(url_for('sponsor_dashboard'))
            elif user.role == 'influencer':
                return redirect(url_for('influencer_dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='scrypt')
        new_user = User(username=form.username.data, password=hashed_password, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('dashboard.html', name=current_user.username)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    # Here you would add logic to gather statistics for the admin
    return render_template('admin_dashboard.html')

@app.route('/sponsor/dashboard')
@login_required
def sponsor_dashboard():
    if current_user.role != 'sponsor':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    # Logic to gather sponsor-specific data
    return render_template('sponsor_dashboard.html')

@app.route('/influencer/dashboard')
@login_required
def influencer_dashboard():
    if current_user.role != 'influencer':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    # Logic to gather influencer-specific data
    return render_template('influencer_dashboard.html')


def create_admin_user():
    admin_username = 'admin'
    admin_password = 'admin123'
    admin_role = 'admin'
    admin = User.query.filter_by(username=admin_username).first()
    if not admin:
        hashed_password = generate_password_hash(admin_password, method='scrypt')
        admin = User(username=admin_username, password=hashed_password, role=admin_role)
        db.session.add(admin)
        db.session.commit()
        print('Admin user created with username: admin and password: adminpass')
    else:
        print('Admin user already exists.')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
    app.run(debug=True)