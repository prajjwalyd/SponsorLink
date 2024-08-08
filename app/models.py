from . import db
from flask_login import UserMixin
from flask_jwt_extended import create_access_token

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'sponsor', 'influencer'
    flagged = db.Column(db.Boolean, default=False)  # Flag for inappropriate users

    campaigns = db.relationship('Campaign', backref='owner', lazy=True, cascade='all, delete-orphan')
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True, cascade='all, delete-orphan')

    # for Sponsors
    company_name = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    budget = db.Column(db.Integer)
    # for Influencer
    category = db.Column(db.String(100)) 
    niche = db.Column(db.String(100))
    followers = db.Column(db.Integer)
    platform = db.Column(db.String(10))

    def get_token(self):
        token = create_access_token(identity=self.id)
        return token

    def __repr__(self):
        return f'<User {self.username}>'

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    start_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    end_date = db.Column(db.DateTime)
    niche = db.Column(db.String(100))
    budget = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    visibility = db.Column(db.String(10))  # public or private
    flagged = db.Column(db.Boolean, default=False)
    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Campaign {self.name}>'

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Float, nullable=False)
    negotiation_comment = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Requested')
    flagged = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<AdRequest {self.id}>'