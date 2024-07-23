from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

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
    flagged = db.Column(db.Boolean, default=False)  # Flag for inappropriate users

    campaigns = db.relationship('Campaign', backref='owner', lazy=True)
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)

    # Sponsor fields
    company_name = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    budget = db.Column(db.Integer)
    # Influencer fields
    category = db.Column(db.String(100)) # Health, Gaming, etc.
    niche = db.Column(db.String(100))
    reach = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    platform = db.Column(db.String(10))
    def __repr__(self):
        return f'<User {self.username}>'

# Define Campaign model
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    start_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    end_date = db.Column(db.DateTime)
    niche = db.Column(db.String(100))
    budget = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    visibility = db.Column(db.String(10))  # 'public' or 'private'
    flagged = db.Column(db.Boolean, default=False)
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
    status = db.Column(db.String(20), nullable=False, default='Requested')

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
    # status = SelectField('Status', choices=[
    #     ('Requested', 'Requested'),
    #     ('Accepted', 'Accepted'),
    #     ('Rejected', 'Rejected'),
    #     ('Negotiated', 'Negotiated')
    # ], validators=[DataRequired()])
    negotiation_comment = TextAreaField('Negotiation Comment', validators=[Optional()])
    submit = SubmitField('Save Ad Request')


class SponsorProfileForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    industry = StringField('Industry', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class InfluencerProfileForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    niche = StringField('Niche', validators=[DataRequired()])
    reach = FloatField('Reach', validators=[DataRequired()])
    submit = SubmitField('Update Profile')



class InfluencerSearchForm(FlaskForm):
    niche = StringField('Niche', validators=[Optional()])
    reach_min = FloatField('Min Reach', validators=[Optional()])
    reach_max = FloatField('Max Reach', validators=[Optional()])
    submit = SubmitField('Search')

class CampaignSearchForm(FlaskForm):
    niche = StringField('Niche', validators=[Optional()])
    submit = SubmitField('Search')






# # Define Routes
# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'sponsor':
            return redirect(url_for('sponsor_dashboard'))
        elif current_user.role == 'influencer':
            return redirect(url_for('influencer_dashboard'))
    return render_template('index.html')


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

@app.route('/admin_dashboard')
def admin_dashboard():
    users = User.query.all()
    campaigns = Campaign.query.all()
    flagged_users = User.query.filter_by(flagged=True).all()
    flagged_campaigns = Campaign.query.filter_by(flagged=True).all()

    statistics = {
        'active_users': User.query.count(),  # Fixed to show total users
        'total_campaigns': Campaign.query.count(),
        'public_campaigns': Campaign.query.filter_by(visibility='public').count(),
        'private_campaigns': Campaign.query.filter_by(visibility='private').count(),
        'total_ad_requests': AdRequest.query.count(),
        'accepted_requests': AdRequest.query.filter_by(status='Accepted').count(),
        'rejected_requests': AdRequest.query.filter_by(status='Rejected').count(),
        'negotiated_requests': AdRequest.query.filter_by(status='Negotiated').count(),
    }

    return render_template(
        'admin_dashboard.html',
        users=users,
        campaigns=campaigns,
        flagged_users=flagged_users,
        flagged_campaigns=flagged_campaigns,
        **statistics
    )


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
    requested_ads = AdRequest.query.filter_by(influencer_id=current_user.id, status='Requested').all()
    current_ads = AdRequest.query.filter_by(influencer_id=current_user.id, status='Accepted').all()
    negotiated_ads = AdRequest.query.filter_by(influencer_id=current_user.id, status='Negotiated').all()
    return render_template('influencer_dashboard.html', current_ads=current_ads, negotiated_ads=negotiated_ads, requested_ads=requested_ads)


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
            # status=form.status.data
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
        ad_request.status = 'Requested'  # Reset the status to 'Requested'
        db.session.commit()
        flash('Your ad request has been updated and marked as Requested.', 'success')
        return redirect(url_for('sponsor_dashboard'))
    elif request.method == 'GET':
        form.campaign_id.data = ad_request.campaign_id
        form.influencer_id.data = ad_request.influencer_id
        form.requirements.data = ad_request.requirements
        form.payment_amount.data = ad_request.payment_amount
        # form.status.data = ad_request.status
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

@app.route('/negotiate_ad_request/<int:ad_request_id>', methods=['GET', 'POST'])
@login_required
def negotiate_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    form = AdRequestForm(obj=ad_request)
    form.campaign_id.choices = [(ad_request.campaign_id, ad_request.campaign.name)]
    form.influencer_id.choices = [(ad_request.influencer_id, ad_request.influencer.username)]

    if form.validate_on_submit():
        ad_request.requirements = form.requirements.data
        ad_request.payment_amount = form.payment_amount.data
        ad_request.negotiation_comment = form.negotiation_comment.data
        ad_request.status = 'Negotiated'
        db.session.commit()
        flash('Ad request has been negotiated.', 'success')
        return redirect(url_for('influencer_dashboard'))
    return render_template('negotiate_ad_request.html', legend='Negotiate Ad Request', form=form)





@app.route('/flag_user/<int:user_id>', methods=['POST'])
def flag_user(user_id):
    user = User.query.get(user_id)
    user.flagged = True
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/remove_flag_user/<int:user_id>', methods=['POST'])
def remove_flag_user(user_id):
    user = User.query.get(user_id)
    user.flagged = False
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/flag_campaign/<int:campaign_id>', methods=['POST'])
def flag_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    campaign.flagged = True
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/remove_flag_campaign/<int:campaign_id>', methods=['POST'])
def remove_flag_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    campaign.flagged = False
    db.session.commit()
    return redirect(url_for('admin_dashboard'))





@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role == 'sponsor':
        form = SponsorProfileForm()
        if form.validate_on_submit():
            current_user.company_name = form.company_name.data
            current_user.industry = form.industry.data
            current_user.budget = form.budget.data
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('sponsor_dashboard'))
        elif request.method == 'GET':
            form.company_name.data = current_user.company_name
            form.industry.data = current_user.industry
            form.budget.data = current_user.budget
        return render_template('profile.html', form=form)
    
    elif current_user.role == 'influencer':
        form = InfluencerProfileForm()
        if form.validate_on_submit():
            current_user.category = form.category.data
            current_user.niche = form.niche.data
            current_user.reach = form.reach.data
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('influencer_dashboard'))
        elif request.method == 'GET':
            form.category.data = current_user.category
            form.niche.data = current_user.niche
            form.reach.data = current_user.reach
        return render_template('profile.html', form=form)
    
    else:
        flash('Admins cannot update profiles', 'danger')
        return redirect(url_for('index'))




@app.route('/search_influencers', methods=['GET', 'POST'])
@login_required
def search_influencers():
    if current_user.role != 'sponsor':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    form = InfluencerSearchForm()
    influencers = []
    if form.validate_on_submit():
        query = User.query.filter_by(role='influencer')
        if form.niche.data:
            query = query.filter(User.niche.ilike(f"%{form.niche.data}%"))
        if form.reach_min.data:
            query = query.filter(User.reach >= form.reach_min.data)
        if form.reach_max.data:
            query = query.filter(User.reach <= form.reach_max.data)
        influencers = query.all()
    return render_template('search_influencers.html', form=form, influencers=influencers)

@app.route('/search_campaigns', methods=['GET', 'POST'])
@login_required
def search_campaigns():
    if current_user.role != 'influencer':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('index'))
    form = CampaignSearchForm()
    campaigns = []
    if form.validate_on_submit():
        query = Campaign.query.filter_by(visibility='public')
        if form.niche.data:
            query = query.join(User).filter(User.niche.ilike(f"%{form.niche.data}%"))
        campaigns = query.all()
    return render_template('search_campaigns.html', form=form, campaigns=campaigns)










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