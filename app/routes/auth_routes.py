from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.forms import LoginForm, RegistrationForm, InfluencerRegistrationForm, SponsorRegistrationForm
from app import db, login_manager

bp = Blueprint('auth', __name__)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'sponsor':
            return redirect(url_for('user.sponsor_dashboard'))
        elif current_user.role == 'influencer':
            return redirect(url_for('user.influencer_dashboard'))
    return render_template('index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.username == 'admin':
            flash('Unauthorized!', 'danger')
        elif user and check_password_hash(user.password, form.password.data):
            # token = user.get_token()
            # return jsonify({'token': token}), 200
            login_user(user)
            flash('Logged in successfully!', 'success')
            if user.role == 'sponsor':
                return redirect(url_for('user.sponsor_dashboard'))
            elif user.role == 'influencer':
                return redirect(url_for('user.influencer_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.role == 'admin' and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Admin logged in successfully!', 'success')
            return redirect(url_for('user.admin_dashboard'))
        else:
            flash('Invalid admin username or password', 'danger')
    return render_template('admin_login.html', form=form)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = generate_password_hash(form.password.data, method='scrypt')
#         new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Account created successfully! Please log in.', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        if user_type == 'sponsor':
            return redirect(url_for('auth.register_sponsor'))
        elif user_type == 'influencer':
            return redirect(url_for('auth.register_influencer'))
        else:
            return "Error: Invalid user type selected", 400
    return render_template('user_selection.html')


@bp.route('/register/sponsor', methods=['GET', 'POST'])
def register_sponsor():
    form = SponsorRegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='scrypt')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role='sponsor',
            company_name=form.company_name.data,
            industry=form.industry.data,
            budget=form.budget.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Sponsor account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register_sponsor.html', form=form)

@bp.route('/register/influencer', methods=['GET', 'POST'])
def register_influencer():
    form = InfluencerRegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='scrypt')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role='influencer',
            category=form.category.data,
            niche=form.niche.data,
            followers=form.followers.data,
            platform=form.platform.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Influencer account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register_influencer.html', form=form)



@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.home'))
