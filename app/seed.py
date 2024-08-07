# app/seed.py
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
    # Check if there are any users other than the admin
    if User.query.filter(User.username != 'admin').count() == 0:
        users = [
            User(username='sponsor1', email='sponsor1@gmail.com', password=generate_password_hash('password', method='scrypt'), role='sponsor', company_name='TechCorp', industry='Technology', budget=100000),
            User(username='sponsor2', email='sponsor2@gmail.com', password=generate_password_hash('password', method='scrypt'), role='sponsor', company_name='HealthPlus', industry='Healthcare', budget=150000),
            User(username='sponsor3', email='sponsor3@gmail.com', password=generate_password_hash('password', method='scrypt'), role='sponsor', company_name='EcoHome', industry='Home Goods', budget=120000),
            User(username='influencer1', email='influencer1@gmail.com', password=generate_password_hash('password', method='scrypt'), role='influencer', category='Fitness', niche='Yoga', followers=20000, platform='YouTube'),
            User(username='influencer2', email='influencer2@gmail.com', password=generate_password_hash('password', method='scrypt'), role='influencer', category='Food', niche='Vegan', followers=10000, platform='Instagram'),
            User(username='influencer3', email='influencer3@gmail.com', password=generate_password_hash('password', method='scrypt'), role='influencer', category='Travel', niche='Adventure', followers=40000, platform='YouTube'),
            User(username='influencer4', email='influencer4@gmail.com', password=generate_password_hash('password', method='scrypt'), role='influencer', category='Fashion', niche='Streetwear', followers=15000, platform='Instagram')
        ]

        campaigns = [
            Campaign(name='TechLaunch', description='Launch of the new TechCorp gadget, featuring innovative AI technology.', budget=50000, owner_id=2, visibility='public', niche='Technology'),
            Campaign(name='Wellness Week', description='A week-long campaign promoting HealthPlus wellness products.', budget=80000, owner_id=3, visibility='private', niche='Health'),
            Campaign(name='EcoHome Challenge', description='Challenge to promote EcoHome sustainable living products.', budget=70000, owner_id=4, visibility='public', niche='Sustainability'),
            Campaign(name='Fashion Fiesta', description='A vibrant campaign promoting the latest in streetwear fashion.', budget=40000, owner_id=4, visibility='public', niche='Fashion')
        ]

        ad_requests = [
            AdRequest(campaign_id=1, influencer_id=5, name='Instagram Reel Promotion', requirements='Create a dynamic Instagram reel showcasing the features of our new gadget.', payment_amount=5000, status='Requested'),
            AdRequest(campaign_id=1, influencer_id=5, name='YouTube Unboxing Video', requirements='Produce a detailed unboxing video for our new tech product on YouTube.', payment_amount=8000, status='Accepted'),
            AdRequest(campaign_id=2, influencer_id=6, name='Vegan Recipe Video', requirements='Create a vegan recipe video featuring HealthPlus products.', payment_amount=6000, status='Negotiated', negotiation_comment='Require higher payment due to video complexity.'),
            AdRequest(campaign_id=2, influencer_id=6, name='Instagram Stories Series', requirements='Post a series of Instagram stories discussing the benefits of our wellness products.', payment_amount=4000, status='Requested'),
            AdRequest(campaign_id=3, influencer_id=7, name='Adventure Vlog Series', requirements='Create a vlog series highlighting sustainable travel practices with EcoHome products.', payment_amount=7000, status='Accepted'),
            AdRequest(campaign_id=3, influencer_id=7, name='Blog Post on Sustainability', requirements='Write an in-depth blog post about the importance of sustainability and EcoHome’s role.', payment_amount=3000, status='Requested'),
            AdRequest(campaign_id=4, influencer_id=8, name='Streetwear Fashion Haul', requirements='Produce a fashion haul video showcasing our latest streetwear collection.', payment_amount=5000, status='Requested'),
            AdRequest(campaign_id=4, influencer_id=8, name='Instagram Post', requirements='Create a stylish Instagram post featuring our streetwear collection.', payment_amount=2500, status='Requested'),
            AdRequest(campaign_id=4, influencer_id=8, name='YouTube Video Series', requirements='Produce a YouTube video series showcasing our latest streetwear collection.', payment_amount=5500, status='Requested'),
            AdRequest(campaign_id=4, influencer_id=8, name='Instagram Post', requirements='Create a stylish Instagram post featuring our streetwear collection.', payment_amount=2500, status='Rejected')
        ]

        db.session.add_all(users)
        db.session.add_all(campaigns)
        db.session.add_all(ad_requests)
        db.session.commit()
        print("Database seeded with sample data.")
    else:
        print("Database already seeded.")

