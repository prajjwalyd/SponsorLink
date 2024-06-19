from app import app, db
from models import User, Campaign

with app.app_context():
    # Create some users
    admin = User(username='admin', password='adminpass', role='admin')
    sponsor = User(username='sponsor1', password='sponsorpass', role='sponsor', company_name='Company A', industry='Tech', budget=10000)
    influencer = User(username='influencer1', password='influencerpass', role='influencer', category='Tech', niche='Gadgets', reach=50000)

    db.session.add(admin)
    db.session.add(sponsor)
    db.session.add(influencer)
    db.session.commit()

    # Create a campaign
    campaign = Campaign(name='Tech Campaign', description='Promote new tech products', budget=5000, visibility='public', sponsor_id=sponsor.id)
    db.session.add(campaign)
    db.session.commit()
    
    print("Database seeded successfully.")
