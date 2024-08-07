from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, Campaign, AdRequest
from app import db

bp = Blueprint('admin', __name__)



@bp.route('/flag_user/<int:user_id>', methods=['POST'])
def flag_user(user_id):
    user = User.query.get(user_id)
    user.flagged = True
    db.session.commit()
    return redirect(url_for('user.admin_dashboard'))

@bp.route('/remove_flag_user/<int:user_id>', methods=['POST'])
def remove_flag_user(user_id):
    user = User.query.get(user_id)
    user.flagged = False
    db.session.commit()
    return redirect(url_for('user.admin_dashboard'))

@bp.route('/flag_campaign/<int:campaign_id>', methods=['POST'])
def flag_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    campaign.flagged = True
    db.session.commit()
    return redirect(url_for('user.admin_dashboard'))

@bp.route('/remove_flag_campaign/<int:campaign_id>', methods=['POST'])
def remove_flag_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    campaign.flagged = False
    db.session.commit()
    return redirect(url_for('user.admin_dashboard'))

@bp.route('/delete_flagged_campaign/<int:campaign_id>', methods=['POST'])
@login_required
def delete_flagged_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign:
        db.session.delete(campaign)
        db.session.commit()
    return redirect(url_for('user.admin_dashboard'))

@bp.route('/delete_flagged_user/<int:user_id>', methods=['POST'])
@login_required
def delete_flagged_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('user.admin_dashboard'))


@bp.route('/flag_ad_request/<int:ad_request_id>', methods=['POST'])
@login_required
def flag_ad_request(ad_request_id):
    ad_request = AdRequest.query.get(ad_request_id)
    if ad_request:
        ad_request.flagged = True
        db.session.commit()
    return redirect(url_for('user.admin_dashboard'))

@bp.route('/remove_flag_ad_request/<int:ad_request_id>', methods=['POST'])
@login_required
def remove_flag_ad_request(ad_request_id):
    ad_request = AdRequest.query.get(ad_request_id)
    if ad_request:
        ad_request.flagged = False
        db.session.commit()
    return redirect(url_for('user.admin_dashboard'))

@bp.route('/delete_flagged_ad_request/<int:ad_request_id>', methods=['POST'])
@login_required
def delete_flagged_ad_request(ad_request_id):
    ad_request = AdRequest.query.get(ad_request_id)
    if ad_request:
        db.session.delete(ad_request)
        db.session.commit()
    return redirect(url_for('user.admin_dashboard'))