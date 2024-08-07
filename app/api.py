from flask import Blueprint, jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from app import db
from app.models import User, Campaign

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/get_token', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Invalid input'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        if user.username == 'admin':
            return jsonify({'error': 'Unauthorized!'}), 403
        token = create_access_token(identity=user.id)
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid username or password'}), 401

class PublicCampaignsAPI(Resource):
    def get(self):
        campaigns = Campaign.query.filter_by(visibility='public').all()
        return jsonify([{
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'niche': campaign.niche,
            'budget': campaign.budget
        } for campaign in campaigns])

class PublicInfluencersAPI(Resource):
    def get(self):
        influencers = User.query.filter_by(role='influencer').all()
        return jsonify([{
            'id': influencer.id,
            'username': influencer.username,
            'category': influencer.category,
            'niche': influencer.niche,
            'followers': influencer.followers,
            'platform': influencer.platform
        } for influencer in influencers])

class CampaignsAPI(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        campaigns = Campaign.query.filter_by(owner_id=current_user_id).all()
        return jsonify([{
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'niche': campaign.niche,
            'budget': campaign.budget,
            'visibility': campaign.visibility
        } for campaign in campaigns])

    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user_id = get_jwt_identity()
        new_campaign = Campaign(
            name=data['name'],
            description=data['description'],
            niche=data['niche'],
            budget=data['budget'],
            visibility=data['visibility'],
            owner_id=current_user_id
        )
        db.session.add(new_campaign)
        db.session.commit()
        return jsonify({'message': 'Campaign created successfully'})

    @jwt_required()
    def delete(self):
        data = request.get_json()
        current_user_id = get_jwt_identity()
        campaign = Campaign.query.filter_by(name=data['name'], owner_id=current_user_id).first()
        if campaign:
            db.session.delete(campaign)
            db.session.commit()
            return jsonify({'message': 'Campaign deleted successfully'})
        return jsonify({'message': 'Campaign not found'}), 404

def register_resources(api):
    api.add_resource(PublicCampaignsAPI, '/api/public/campaigns')
    api.add_resource(PublicInfluencersAPI, '/api/public/influencers')
    api.add_resource(CampaignsAPI, '/api/campaigns')
