from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.extensions import db
from app.models import User, Business
from app.forms import RegistrationForm, LoginForm
from app.config import Config

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Hasaba alyş
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()
        business = Business(
            user_id=user.id,
            name=form.business_name.data,
            slug=form.business_name.data.lower().replace(' ', '-') + '-' + str(user.id)
        )
        db.session.add(business)
        db.session.commit()
        flash('Hasap döredildi! Indi içeri giriň.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

# Adaty ulanyjy girişi (admin üçin işlemez)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.id == Config.ADMIN_ID:
            return redirect(url_for('admin.index'))
        return redirect(url_for('dashboard.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # Eger admin bolsa, bu ýerde girmäge ýol berme
            if user.id == Config.ADMIN_ID:
                flash('Admin üçin aýratyn giriş sahypasy bar: /admin/login', 'warning')
                return redirect(url_for('admin.admin_login'))
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        flash('Email ýa-da parol ýalňyş.', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Çykdyňyz.', 'info')
    return redirect(url_for('public.index'))