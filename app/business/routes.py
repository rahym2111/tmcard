from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Business, Product
from app.forms import BusinessForm, ProductForm
from app.utils import save_uploaded_file
import os

business_bp = Blueprint('business', __name__, url_prefix='/business')

# Biznes döret
@business_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if Business.query.filter_by(user_id=current_user.id).first():
        flash('Siz eýýäm biznes döredipsiňiz.', 'warning')
        return redirect(url_for('dashboard.index'))
    form = BusinessForm()
    if form.validate_on_submit():
        business = Business(
            user_id=current_user.id,
            name=form.name.data,
            slug=form.name.data.lower().replace(' ', '-') + '-' + str(current_user.id),
            category=form.category.data,
            description=form.description.data,
            phone=form.phone.data,
            whatsapp=form.whatsapp.data,
            email=form.email.data,
            instagram=form.instagram.data,
            tiktok=form.tiktok.data,
            telegram=form.telegram.data,
            address=form.address.data,
            maps_link=form.maps_link.data,
            opening_time=form.opening_time.data,
            closing_time=form.closing_time.data
        )
        db.session.add(business)
        db.session.commit()
        flash('Biznes profili döredildi!', 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('business/create.html', form=form)

# Biznes redaktirle
@business_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    business = Business.query.get_or_404(id)
    if business.user_id != current_user.id and current_user.id != 1:
        abort(403)
    form = BusinessForm(obj=business)
    if form.validate_on_submit():
        business.name = form.name.data
        business.category = form.category.data
        business.description = form.description.data
        business.phone = form.phone.data
        business.whatsapp = form.whatsapp.data
        business.email = form.email.data
        business.instagram = form.instagram.data
        business.tiktok = form.tiktok.data
        business.telegram = form.telegram.data
        business.address = form.address.data
        business.maps_link = form.maps_link.data
        business.opening_time = form.opening_time.data
        business.closing_time = form.closing_time.data
        db.session.commit()
        flash('Üýtgetmeler saklandy.', 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('business/edit.html', form=form, business=business)

# Jemgyýetçilik sahypasy (görüş hasaplaýjy)
@business_bp.route('/public/<slug>')
def public(slug):
    business = Business.query.filter_by(slug=slug).first_or_404()
    business.views += 1
    db.session.commit()
    products = Product.query.filter_by(business_id=business.id).all()
    return render_template('business/public.html', business=business, products=products)