from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms import PaymentForm, SponsorProfileForm, InfluencerProfileForm, CampaignSearchForm, InfluencerSearchForm
from app.models import User, AdRequest, Campaign
from app import db

bp = Blueprint('user', __name__)

@bp.route('/admin_dashboard')
def admin_dashboard():
    users = User.query.all()
    campaigns = Campaign.query.all()
    ad_requests = AdRequest.query.all()
    flagged_users = User.query.filter_by(flagged=True).all()
    flagged_campaigns = Campaign.query.filter_by(flagged=True).all()
    flagged_ad_requests = AdRequest.query.filter_by(flagged=True).all()

    statistics = {
        'active_users': User.query.count(),  # Fixed to show total users
        'total_campaigns': Campaign.query.count(),
        'public_campaigns': Campaign.query.filter_by(visibility='public').count(),
        'private_campaigns': Campaign.query.filter_by(visibility='private').count(),
        'total_ad_requests': AdRequest.query.count(),
        'accepted_requests': AdRequest.query.filter_by(status='Accepted').count(),
        'rejected_requests': AdRequest.query.filter_by(status='Rejected').count(),
        'negotiated_requests': AdRequest.query.filter_by(status='Negotiated').count(),
        'requested_requests': AdRequest.query.filter_by(status='Requested').count()
    }

    return render_template(
        'admin_dashboard.html',
        users=users,
        campaigns=campaigns,
        ad_requests=ad_requests,
        flagged_users=flagged_users,
        flagged_campaigns=flagged_campaigns,
        flagged_ad_requests=flagged_ad_requests,
        **statistics
    )


@bp.route('/sponsor_dashboard')
@login_required
def sponsor_dashboard():
    if current_user.role != 'sponsor':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))
    campaigns = Campaign.query.filter_by(owner_id=current_user.id).all()
    ad_requests = AdRequest.query.join(Campaign).filter(Campaign.owner_id == current_user.id).all()
    return render_template('sponsor_dashboard.html', campaigns=campaigns, ad_requests=ad_requests)


@bp.route('/influencer_dashboard')
@login_required
def influencer_dashboard():
    if current_user.role != 'influencer':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))
    requested_ads = AdRequest.query.filter_by(influencer_id=current_user.id, status='Requested').all()
    current_ads = AdRequest.query.filter_by(influencer_id=current_user.id, status='Accepted').all()
    negotiated_ads = AdRequest.query.filter_by(influencer_id=current_user.id, status='Negotiated').all()
    return render_template('influencer_dashboard.html', current_ads=current_ads, negotiated_ads=negotiated_ads, requested_ads=requested_ads)


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role == 'sponsor':
        form = SponsorProfileForm()
        if form.validate_on_submit():
            current_user.company_name = form.company_name.data
            current_user.industry = form.industry.data
            current_user.budget = form.budget.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user.sponsor_dashboard'))
        elif request.method == 'GET':
            form.company_name.data = current_user.company_name
            form.industry.data = current_user.industry
            form.budget.data = current_user.budget
            form.email.data = current_user.email
        return render_template('profile.html', form=form)
    
    elif current_user.role == 'influencer':
        form = InfluencerProfileForm()
        if form.validate_on_submit():
            current_user.category = form.category.data
            current_user.niche = form.niche.data
            current_user.followers = form.followers.data
            current_user.platform = form.platform.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user.influencer_dashboard'))
        elif request.method == 'GET':
            form.category.data = current_user.category
            form.niche.data = current_user.niche
            form.followers.data = current_user.followers
            form.platform.data = current_user.platform
            form.email.data = current_user.email
        return render_template('profile.html', form=form)
    
    else:
        flash('Admins cannot update profiles', 'danger')
        return redirect(url_for('auth.home'))


@bp.route('/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile_page.html', user=user)

@bp.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    form = PaymentForm()
    if form.validate_on_submit():
        # Process payment here
        # dummy
        flash('Payment processed successfully!', 'success')
        return redirect(url_for('user.sponsor_dashboard'))
    
    return render_template('payment.html', form=form)




@bp.route('/search_influencers', methods=['GET', 'POST'])
@login_required
def search_influencers():
    if current_user.role != 'sponsor':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))
    form = InfluencerSearchForm()
    influencers = []
    if form.validate_on_submit():
        query = User.query.filter_by(role='influencer')
        if form.niche.data:
            query = query.filter(User.niche.ilike(f"%{form.niche.data}%"))
        if form.platform.data:
            query = query.filter(User.platform.ilike(f"%{form.platform.data}%"))
        
        if form.reach_min.data:
            query = query.filter(User.reach >= form.reach_min.data)
        if form.followers_min.data:
            query = query.filter(User.followers >= form.followers_min.data)
        
        influencers = query.all()
    return render_template('search_influencers.html', form=form, influencers=influencers)

@bp.route('/search_campaigns', methods=['GET', 'POST'])
@login_required
def search_campaigns():
    if current_user.role != 'influencer':
        flash('Access unauthorized!', 'danger')
        return redirect(url_for('auth.home'))
    
    form = CampaignSearchForm()
    campaigns = []
    
    if form.validate_on_submit():
        query = Campaign.query.filter_by(visibility='public').join(User, User.id == Campaign.owner_id)
        
        if form.niche.data:
            query = query.filter(Campaign.niche.ilike(f"%{form.niche.data}%"))
        if form.min_budget.data:
            query = query.filter(Campaign.budget >= form.min_budget.data)
        
        campaigns = query.all()
    
    return render_template('search_campaigns.html', form=form, campaigns=campaigns)
