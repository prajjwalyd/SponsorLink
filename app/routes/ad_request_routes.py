from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms import AdRequestForm
from app.models import AdRequest, Campaign, User
from app import db

bp = Blueprint('ad_request', __name__)


@bp.route('/ad_request/new/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def create_ad_request(campaign_id):
    if current_user.role != 'sponsor':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))

    # Check if the campaign belongs to the current user
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.owner_id != current_user.id:
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))

    form = AdRequestForm()
    form.campaign_id.choices = [(campaign.id, campaign.name)]  # Pre-select the campaign
    form.campaign_id.data = campaign.id  # Pre-set the campaign ID
    form.influencer_id.choices = [(influencer.id, influencer.username) for influencer in User.query.filter_by(role='influencer').all()]

    if form.validate_on_submit():
        ad_request = AdRequest(
            campaign_id=campaign.id,
            influencer_id=form.influencer_id.data,
            name=form.name.data,
            requirements=form.requirements.data,
            payment_amount=form.payment_amount.data,
        )
        db.session.add(ad_request)
        db.session.commit()
        flash('Ad request created successfully!', 'success')
        return redirect(url_for('user.sponsor_dashboard'))

    return render_template('create_ad_request.html', form=form)
    
@bp.route('/ad_request/<int:ad_request_id>/update', methods=['GET', 'POST'])
@login_required
def update_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    # Check if the user is the owner or an admin
    if ad_request.campaign.owner != current_user and not current_user.role == 'admin':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))
    form = AdRequestForm()
    form.campaign_id.choices = [(campaign.id, campaign.name) for campaign in current_user.campaigns]
    form.influencer_id.choices = [(influencer.id, influencer.username) for influencer in User.query.filter_by(role='influencer').all()]
    if form.validate_on_submit():
        ad_request.campaign_id = form.campaign_id.data
        ad_request.influencer_id = form.influencer_id.data
        ad_request.name = form.name.data
        ad_request.requirements = form.requirements.data
        ad_request.payment_amount = form.payment_amount.data
        ad_request.status = 'Requested'  # Reset the status to 'Requested'
        db.session.commit()
        flash('Your ad request has been updated and marked as Requested.', 'success')
        return redirect(url_for('user.sponsor_dashboard'))
    elif request.method == 'GET':
        form.campaign_id.data = ad_request.campaign_id
        form.influencer_id.data = ad_request.influencer_id
        form.name.data = ad_request.name
        form.requirements.data = ad_request.requirements
        form.payment_amount.data = ad_request.payment_amount
        # form.status.data = ad_request.status
    return render_template('create_ad_request.html', form=form, legend='Update Ad Request')

@bp.route('/ad_request/<int:ad_request_id>/delete', methods=['POST'])
@login_required
def delete_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.campaign.owner != current_user:
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))
    db.session.delete(ad_request)
    db.session.commit()
    flash('Ad request deleted successfully!', 'success')
    return redirect(url_for('user.sponsor_dashboard'))



@bp.route('/ad_request/<int:ad_request_id>/accept', methods=['POST'])
@login_required
def accept_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.influencer != current_user:
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))
    ad_request.status = 'Accepted'
    db.session.commit()
    flash('Ad request accepted!', 'success')
    return redirect(url_for('user.influencer_dashboard'))

@bp.route('/ad_request/<int:ad_request_id>/reject', methods=['POST'])
@login_required
def reject_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.influencer != current_user:
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))
    ad_request.status = 'Rejected'
    db.session.commit()
    flash('Ad request rejected!', 'danger')
    return redirect(url_for('user.influencer_dashboard'))

@bp.route('/negotiate_ad_request/<int:ad_request_id>', methods=['GET', 'POST'])
@login_required
def negotiate_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    form = AdRequestForm(obj=ad_request)
    form.campaign_id.choices = [(ad_request.campaign_id, ad_request.campaign.name)]
    form.influencer_id.choices = [(ad_request.influencer_id, ad_request.influencer.username)]

    if form.validate_on_submit():
        ad_request.requirements = form.requirements.data
        ad_request.payment_amount = form.payment_amount.data
        ad_request.negotiation_comment = form.negotiation_comment.data
        ad_request.status = 'Negotiated'
        db.session.commit()
        flash('Ad request has been negotiated.', 'success')
        return redirect(url_for('user.influencer_dashboard'))
    return render_template('negotiate_ad_request.html', legend='Negotiate Ad Request', form=form)

@bp.route('/ad_request/new/<int:influencer_id>', methods=['GET', 'POST'])
@login_required
def create_ad_request_for_influencer(influencer_id):
    if current_user.role != 'sponsor':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))
    form = AdRequestForm()
    form.campaign_id.choices = [(campaign.id, campaign.name) for campaign in current_user.campaigns]
    form.influencer_id.choices = [(influencer_id, User.query.get(influencer_id).username)]
    if form.validate_on_submit():
        ad_request = AdRequest(
            campaign_id=form.campaign_id.data,
            influencer_id=form.influencer_id.data,
            name = form.name.data,
            requirements=form.requirements.data,
            payment_amount=form.payment_amount.data,
        )
        db.session.add(ad_request)
        db.session.commit()
        flash('Ad request created successfully!', 'success')
        return redirect(url_for('user.sponsor_dashboard'))
    return render_template('create_ad_request.html', form=form)

