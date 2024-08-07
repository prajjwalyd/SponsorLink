from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms import CampaignForm
from app.models import Campaign
from app import db

bp = Blueprint('campaign', __name__)


@bp.route('/campaign/new', methods=['GET', 'POST'])
@login_required
def create_campaign():
    if current_user.role != 'sponsor':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))
    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            budget=form.budget.data,
            niche = form.niche.data,
            visibility=form.visibility.data,
            owner_id=current_user.id 
        )
        db.session.add(campaign)
        db.session.commit()
        flash('Campaign created successfully!', 'success')
        return redirect(url_for('user.sponsor_dashboard'))
    return render_template('create_campaign.html', form=form)

@bp.route('/campaign/<int:campaign_id>/update', methods=['GET', 'POST'])
@login_required
def update_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.owner != current_user:
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))
    form = CampaignForm()
    if form.validate_on_submit():
        campaign.name = form.name.data
        campaign.description = form.description.data
        campaign.start_date = form.start_date.data
        campaign.end_date = form.end_date.data
        campaign.budget = form.budget.data
        campaign.niche = form.niche.data
        campaign.visibility = form.visibility.data
        db.session.commit()
        flash('Campaign updated successfully!', 'success')
        return redirect(url_for('user.sponsor_dashboard'))
    elif request.method == 'GET':
        form.name.data = campaign.name
        form.description.data = campaign.description
        form.start_date.data = campaign.start_date
        form.end_date.data = campaign.end_date
        form.budget.data = campaign.budget
        form.niche.data = campaign.niche
        form.visibility.data = campaign.visibility
    return render_template('create_campaign.html', form=form, legend='Update Campaign')

@bp.route('/campaign/<int:campaign_id>/delete', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.owner != current_user:
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign deleted successfully!', 'success')
    return redirect(url_for('user.sponsor_dashboard'))

