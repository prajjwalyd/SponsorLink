# 🔗SponsorLink
### Influencer Engagement and Sponsorship Coordination Platform
It's a platform to connect Sponsors and Influencers so that sponsors can get their product/service advertised and influencers can get monetary benefit.

## Directory Structure
```
SponsorLink/
│
├── app/
│   ├── __init__.py
|   ├── api.py
│   ├── models.py
│   ├── forms.py
|   ├── seed.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── admin_routes.py
│   │   ├── campaign_routes.py
│   │   ├── ad_request_routes.py
│   └── templates/
│       ├── index.html
│       ├── layout.html
│       ├── ... more
├── app.db
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

## Setup Instructions

Install Requirements:
```
pip install -r requirements.txt
```

Run the App:
```
python app.py
```