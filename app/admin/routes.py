from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User, Business, Product
from app.forms import AdminLoginForm
from app.config import Config

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if current_user.id == Config.ADMIN_ID:
            return redirect(url_for('admin.index'))
        flash('Siz admin dälsiňiz.', 'danger')
        return redirect(url_for('auth.login'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data) and user.id == Config.ADMIN_ID:
            login_user(user)
            return redirect(url_for('admin.index'))
        flash('Admin email ýa-da parol ýalňyş.', 'danger')
    return render_template('admin/login.html', form=form)

@admin_bp.route('/')
@login_required
def index():
    if current_user.id != Config.ADMIN_ID:
        flash('Bu sahypa diňe admin üçin.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    search = request.args.get('search', '')
    if search:
        users = User.query.filter(
            User.name.ilike(f'%{search}%') | 
            User.email.ilike(f'%{search}%')
        ).all()
    else:
        users = User.query.all()
    
    total_users = User.query.count()
    total_businesses = Business.query.count()
    total_products = Product.query.count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_businesses = Business.query.order_by(Business.created_at.desc()).limit(5).all()
    
    for user in users:
        user.business_count = len(user.businesses)
    
    businesses = Business.query.all()
    
    return render_template('admin/index.html',
                         users=users,
                         businesses=businesses,
                         total_users=total_users,
                         total_businesses=total_businesses,
                         total_products=total_products,
                         recent_users=recent_users,
                         recent_businesses=recent_businesses,
                         search=search)

@admin_bp.route('/business/delete/<int:id>', methods=['POST'])
@login_required
def delete_business(id):
    if current_user.id != Config.ADMIN_ID:
        flash('Rugsat ýok.', 'danger')
        return redirect(url_for('admin.index'))
    business = Business.query.get_or_404(id)
    db.session.delete(business)
    db.session.commit()
    flash('Biznes öçürildi.', 'success')
    return redirect(url_for('admin.index'))