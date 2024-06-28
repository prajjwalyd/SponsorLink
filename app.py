# app.py

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, FloatField
from wtforms.validators import Optional
from wtforms.validators import DataRequired, Length, EqualTo

# Initialize the app and configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'sponsor', 'influencer'

    campaigns = db.relationship('Campaign', backref='owner', lazy=True)
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)
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
    budget = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    visibility = db.Column(db.String(10))  # 'public' or 'private'
    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)

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
    negotiation_comment = db.Column(db.Text, nullable=True)
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

class CampaignForm(FlaskForm):
    name = StringField('Campaign Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])  # Change from DecimalField to FloatField
    visibility = SelectField('Visibility', choices=[('public', 'Public'), ('private', 'Private')], validators=[DataRequired()])
    submit = SubmitField('Save Campaign')

class AdRequestForm(FlaskForm):
    campaign_id = SelectField('Campaign', coerce=int, validators=[DataRequired()])
    influencer_id = SelectField('Influencer', coerce=int, validators=[DataRequired()])
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    payment_amount = FloatField('Payment Amount', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Negotiated', 'Negotiated'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    negotiation_comment = TextAreaField('Negotiation Comment', validators=[Optional()])
    submit = SubmitField('Save Ad Request')







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

@app.route('/sponsor_dashboard')
@login_required
def sponsor_dashboard():
    if current_user.role != 'sponsor':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    campaigns = Campaign.query.filter_by(owner_id=current_user.id).all()
    ad_requests = AdRequest.query.join(Campaign).filter(Campaign.owner_id == current_user.id).all()
    return render_template('sponsor_dashboard.html', campaigns=campaigns, ad_requests=ad_requests)


@app.route('/influencer_dashboard')
@login_required
def influencer_dashboard():
    if current_user.role != 'influencer':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    ad_requests = AdRequest.query.filter_by(influencer_id=current_user.id).all()
    return render_template('influencer_dashboard.html', ad_requests=ad_requests)

@app.route('/campaign/new', methods=['GET', 'POST'])
@login_required
def create_campaign():
    if current_user.role != 'sponsor':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            budget=form.budget.data,
            visibility=form.visibility.data,
            owner_id=current_user.id  # Use owner_id instead of owner
        )
        db.session.add(campaign)
        db.session.commit()
        flash('Campaign created successfully!', 'success')
        return redirect(url_for('sponsor_dashboard'))
    return render_template('create_campaign.html', form=form)

@app.route('/campaign/<int:campaign_id>/update', methods=['GET', 'POST'])
@login_required
def update_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.owner != current_user:
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    form = CampaignForm()
    if form.validate_on_submit():
        campaign.name = form.name.data
        campaign.description = form.description.data
        campaign.start_date = form.start_date.data
        campaign.end_date = form.end_date.data
        campaign.budget = form.budget.data
        campaign.visibility = form.visibility.data
        db.session.commit()
        flash('Campaign updated successfully!', 'success')
        return redirect(url_for('sponsor_dashboard'))
    elif request.method == 'GET':
        form.name.data = campaign.name
        form.description.data = campaign.description
        form.start_date.data = campaign.start_date
        form.end_date.data = campaign.end_date
        form.budget.data = campaign.budget
        form.visibility.data = campaign.visibility
    return render_template('create_campaign.html', form=form, legend='Update Campaign')

@app.route('/campaign/<int:campaign_id>/delete', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.owner != current_user:
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign deleted successfully!', 'success')
    return redirect(url_for('sponsor_dashboard'))



@app.route('/ad_request/new', methods=['GET', 'POST'])
@login_required
def create_ad_request():
    if current_user.role != 'sponsor':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    form = AdRequestForm()
    form.campaign_id.choices = [(campaign.id, campaign.name) for campaign in current_user.campaigns]
    form.influencer_id.choices = [(influencer.id, influencer.username) for influencer in User.query.filter_by(role='influencer').all()]
    if form.validate_on_submit():
        ad_request = AdRequest(
            campaign_id=form.campaign_id.data,
            influencer_id=form.influencer_id.data,
            requirements=form.requirements.data,
            payment_amount=form.payment_amount.data,
            status=form.status.data
        )
        db.session.add(ad_request)
        db.session.commit()
        flash('Ad request created successfully!', 'success')
        return redirect(url_for('sponsor_dashboard'))
    return render_template('create_ad_request.html', form=form)

@app.route('/ad_request/<int:ad_request_id>/update', methods=['GET', 'POST'])
@login_required
def update_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.campaign.owner != current_user:
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    form = AdRequestForm()
    form.campaign_id.choices = [(campaign.id, campaign.name) for campaign in current_user.campaigns]
    form.influencer_id.choices = [(influencer.id, influencer.username) for influencer in User.query.filter_by(role='influencer').all()]
    if form.validate_on_submit():
        ad_request.campaign_id = form.campaign_id.data
        ad_request.influencer_id = form.influencer_id.data
        ad_request.requirements = form.requirements.data
        ad_request.payment_amount = form.payment_amount.data
        ad_request.status = form.status.data
        db.session.commit()
        flash('Ad request updated successfully!', 'success')
        return redirect(url_for('sponsor_dashboard'))
    elif request.method == 'GET':
        form.campaign_id.data = ad_request.campaign_id
        form.influencer_id.data = ad_request.influencer_id
        form.requirements.data = ad_request.requirements
        form.payment_amount.data = ad_request.payment_amount
        form.status.data = ad_request.status
    return render_template('create_ad_request.html', form=form, legend='Update Ad Request')

@app.route('/ad_request/<int:ad_request_id>/delete', methods=['POST'])
@login_required
def delete_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.campaign.owner != current_user:
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    db.session.delete(ad_request)
    db.session.commit()
    flash('Ad request deleted successfully!', 'success')
    return redirect(url_for('sponsor_dashboard'))



@app.route('/ad_request/<int:ad_request_id>/accept', methods=['POST'])
@login_required
def accept_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.influencer != current_user:
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    ad_request.status = 'Accepted'
    db.session.commit()
    flash('Ad request accepted!', 'success')
    return redirect(url_for('influencer_dashboard'))

@app.route('/ad_request/<int:ad_request_id>/reject', methods=['POST'])
@login_required
def reject_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.influencer != current_user:
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    ad_request.status = 'Rejected'
    db.session.commit()
    flash('Ad request rejected!', 'danger')
    return redirect(url_for('influencer_dashboard'))

@app.route('/ad_request/<int:ad_request_id>/negotiate', methods=['GET', 'POST'])
@login_required
def negotiate_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.influencer != current_user:
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    form = AdRequestForm()
    if form.validate_on_submit():
        ad_request.requirements = form.requirements.data
        ad_request.payment_amount = form.payment_amount.data
        ad_request.negotiation_comment = form.negotiation_comment.data
        ad_request.status = 'Negotiated'
        db.session.commit()
        flash('Ad request sent for negotiation!', 'success')
        return redirect(url_for('influencer_dashboard'))
    elif request.method == 'GET':
        form.requirements.data = ad_request.requirements
        form.payment_amount.data = ad_request.payment_amount
        form.negotiation_comment.data = ad_request.negotiation_comment
    return render_template('negotiate_ad_request.html', form=form, legend='Negotiate Ad Request')











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