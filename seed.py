from app import app, db, User, Campaign, AdRequest
from werkzeug.security import generate_password_hash

def seed_data():
    users = [
        User(username='sponsor1', password=generate_password_hash('password', method='scrypt'), role='sponsor', company_name='TechCorp', industry='Technology', budget=10000),
        User(username='sponsor2', password=generate_password_hash('password', method='scrypt'), role='sponsor', company_name='HealthPlus', industry='Healthcare', budget=15000),
        User(username='sponsor3', password=generate_password_hash('password', method='scrypt'), role='sponsor', company_name='EcoHome', industry='Home Goods', budget=12000),
        User(username='influencer1', password=generate_password_hash('password', method='scrypt'), role='influencer', category='Fitness', niche='Yoga', reach=5000, followers=2000, platform='YouTube'),
        User(username='influencer2', password=generate_password_hash('password', method='scrypt'), role='influencer', category='Food', niche='Vegan', reach=3000, followers=1000, platform='Instagram'),
        User(username='influencer3', password=generate_password_hash('password', method='scrypt'), role='influencer', category='Travel', niche='Adventure', reach=7000, followers=4000, platform='YouTube'),
        User(username='influencer4', password=generate_password_hash('password', method='scrypt'), role='influencer', category='Fashion', niche='Streetwear', reach=6000, followers=1000, platform='Instagram')
    ]

    campaigns = [
        Campaign(name='TechLaunch', description='Launch of new tech gadget', budget=5000, owner_id=2, visibility='public', niche='Technology'),
        Campaign(name='Wellness Week', description='Health and wellness campaign', budget=8000, owner_id=3, visibility='private', niche='Health'),
        Campaign(name='EcoHome Challenge', description='Promote sustainable living products', budget=7000, owner_id=3, visibility='public', niche='Nature'),
        Campaign(name='Fashion Fiesta', description='Streetwear fashion promotion', budget=4000, owner_id=4, visibility='public', niche='Fashion')
    ]

    ad_requests = [
        AdRequest(campaign_id=1, influencer_id=5, requirements='Promote on Instagram', payment_amount=300, status='Requested'),
        AdRequest(campaign_id=1, influencer_id=6, requirements='Write a blog post', payment_amount=200, status='Accepted'),
        AdRequest(campaign_id=2, influencer_id=6, requirements='Create a YouTube video', payment_amount=500, status='Negotiated', negotiation_comment='Need higher payment'),
        AdRequest(campaign_id=3, influencer_id=7, requirements='Instagram stories and post', payment_amount=350, status='Requested'),
        AdRequest(campaign_id=3, influencer_id=7, requirements='Create a travel vlog', payment_amount=400, status='Accepted'),
        AdRequest(campaign_id=4, influencer_id=8, requirements='Fashion haul video', payment_amount=250, status='Requested'),
        AdRequest(campaign_id=4, influencer_id=8, requirements='Streetwear blog post', payment_amount=150, status='Requested'),
        AdRequest(campaign_id=2, influencer_id=8, requirements='Fashion advice video', payment_amount=300, status='Requested')
    ]

    db.session.add_all(users)
    db.session.add_all(campaigns)
    db.session.add_all(ad_requests)
    db.session.commit()
    print("Database seeded with sample data.")

if __name__ == '__main__':
    with app.app_context():
        seed_data()
