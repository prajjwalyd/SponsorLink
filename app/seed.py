from werkzeug.security import generate_password_hash
from app import db
from app.models import User, Campaign, AdRequest

def seed_admin():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            password=generate_password_hash('admin', method='scrypt'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

def seed_data():
    if not User.query.first():
        users = [
            User(username='sponsor1', email='sponsor1@gmail.com', password=generate_password_hash('password', method='scrypt'), role='sponsor', company_name='TechCorp', industry='Technology', budget=10000),
            User(username='sponsor2', email='sponsor2@gmail.com', password=generate_password_hash('password', method='scrypt'), role='sponsor', company_name='HealthPlus', industry='Healthcare', budget=15000),
            User(username='sponsor3', email='sponsor3@gmail.com', password=generate_password_hash('password', method='scrypt'), role='sponsor', company_name='EcoHome', industry='Home Goods', budget=12000),
            User(username='influencer1', email='influencer1@gmail.com', password=generate_password_hash('password', method='scrypt'), role='influencer', category='Fitness', niche='Yoga', followers=2000, platform='YouTube'),
            User(username='influencer2', email='influencer2@gmail.com', password=generate_password_hash('password', method='scrypt'), role='influencer', category='Food', niche='Vegan', followers=1000, platform='Instagram'),
            User(username='influencer3', email='influencer3@gmail.com', password=generate_password_hash('password', method='scrypt'), role='influencer', category='Travel', niche='Adventure', followers=4000, platform='YouTube'),
            User(username='influencer4', email='influencer4@gmail.com', password=generate_password_hash('password', method='scrypt'), role='influencer', category='Fashion', niche='Streetwear', followers=1000, platform='Instagram')
        ]

        campaigns = [
            Campaign(name='TechLaunch', description='Launch of new tech gadget', budget=5000, owner_id=2, visibility='public', niche='Technology'),
            Campaign(name='Wellness Week', description='Health and wellness campaign', budget=8000, owner_id=3, visibility='private', niche='Health'),
            Campaign(name='EcoHome Challenge', description='Promote sustainable living products', budget=7000, owner_id=3, visibility='public', niche='Nature'),
            Campaign(name='Fashion Fiesta', description='Streetwear fashion promotion', budget=4000, owner_id=4, visibility='public', niche='Fashion')
        ]

        ad_requests = [
            AdRequest(campaign_id=1, influencer_id=5, name='Promote on Instagram', requirements='do a short promotion on instagram reels telling more about our product', payment_amount=300, status='Requested'),
            AdRequest(campaign_id=1, influencer_id=6, name='Write a blog post', requirements='write a short blogpost on our product', payment_amount=200, status='Accepted'),
            AdRequest(campaign_id=2, influencer_id=6, name='Create a YouTube video', requirements='create a high quality youtube video for our product', payment_amount=500, status='Negotiated', negotiation_comment='Need higher payment'),
            AdRequest(campaign_id=3, influencer_id=7, name='Instagram stories and post', requirements='do a short promotion on instagram stories and reels telling more about our product', payment_amount=350, status='Requested'),
            AdRequest(campaign_id=3, influencer_id=7, name='Create a travel vlog', requirements='create a travel blog series', payment_amount=400, status='Accepted'),
            AdRequest(campaign_id=4, influencer_id=8, name='Fashion haul video', requirements='do a short fashion hall show', payment_amount=250, status='Requested'),
            AdRequest(campaign_id=4, influencer_id=8, name='Streetwear blog post', requirements='write a short blogpost on streetwear', payment_amount=150, status='Requested'),
            AdRequest(campaign_id=2, influencer_id=8, name='Fashion advice video', requirements='create a fashion advice video', payment_amount=300, status='Requested')
        ]

        db.session.add_all(users)
        db.session.add_all(campaigns)
        db.session.add_all(ad_requests)
        db.session.commit()
        print("Database seeded with sample data.")
    else:
        print("Database already seeded.")
