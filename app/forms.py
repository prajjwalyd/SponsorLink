from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, FloatField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

# Define Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=200)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('sponsor', 'Sponsor'), ('influencer', 'Influencer')], validators=[DataRequired()])
    submit = SubmitField('Register')

class SponsorRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=200)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    company_name = StringField('Company Name', validators=[DataRequired()])
    industry = StringField('Industry', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])
    submit = SubmitField('Register')

class InfluencerRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    category = StringField('Category', validators=[DataRequired()])
    niche = StringField('Niche', validators=[DataRequired()])
    followers = FloatField('Followers', validators=[DataRequired()])
    platform = StringField('Platform', validators=[DataRequired()])
    submit = SubmitField('Register')

class CampaignForm(FlaskForm):
    name = StringField('Campaign Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    niche = StringField('Niche', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])  # Change from DecimalField to FloatField
    visibility = SelectField('Visibility', choices=[('public', 'Public'), ('private', 'Private')], validators=[DataRequired()])
    submit = SubmitField('Save Campaign')

class AdRequestForm(FlaskForm):
    campaign_id = SelectField('Campaign', coerce=int, validators=[DataRequired()])
    influencer_id = SelectField('Influencer', coerce=int, validators=[DataRequired()])
    name = StringField('Ad Request Name', validators=[DataRequired()])
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
    email = EmailField('Email', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired()])
    industry = StringField('Industry', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class InfluencerProfileForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    niche = StringField('Niche', validators=[DataRequired()])
    # reach = FloatField('Reach', validators=[DataRequired()])
    followers = FloatField('Followers', validators=[DataRequired()])
    platform = StringField('Platform', validators=[DataRequired()])

    submit = SubmitField('Update Profile')

class InfluencerSearchForm(FlaskForm):
    platform = StringField('Platform', validators=[Optional()])
    niche = StringField('Niche', validators=[Optional()])
    reach_min = FloatField('Min Reach', validators=[Optional()])
    followers_min = FloatField('Min Followers', validators=[Optional()])
    submit = SubmitField('Search')

class CampaignSearchForm(FlaskForm):
    niche = StringField('Niche', validators=[Optional()])
    min_budget = FloatField('Min Budget', validators=[Optional()])
    submit = SubmitField('Search')

class PaymentForm(FlaskForm):
    payment_amt = FloatField('Payment Amount', validators=[DataRequired()])
    card_number = StringField('Card Number', validators=[DataRequired(), Length(min=16, max=16)])
    expiry_date = StringField('Expiry Date (MM/YY)', validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=3)])
    submit = SubmitField('Initiate Payment')

