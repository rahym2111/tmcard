from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db, csrf
from app.models import Business, Product
from app.forms import ProductForm
from app.utils import generate_qr_code, save_uploaded_file

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    business = Business.query.filter_by(user_id=current_user.id).first()
    if not business:
        return redirect(url_for('business.create'))
    qr_data = generate_qr_code(url_for('business.public', slug=business.slug, _external=True))
    products = Product.query.filter_by(business_id=business.id).all()
    views = business.views
    return render_template('dashboard/index.html', business=business, qr_data=qr_data, products=products, views=views)

@dashboard_bp.route('/products/manage', methods=['GET', 'POST'])
@login_required
def manage_products():
    business = Business.query.filter_by(user_id=current_user.id).first()
    if not business:
        flash('Ilki biznes dörediň.', 'warning')
        return redirect(url_for('business.create'))
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            business_id=business.id,
            name=form.name.data,
            price=form.price.data
        )
        if form.image.data:
            img_path = save_uploaded_file(form.image.data, 'products')
            if img_path:
                product.image = img_path
        db.session.add(product)
        db.session.commit()
        flash('Haryt goşuldy.', 'success')
        return redirect(url_for('dashboard.manage_products'))
    products = Product.query.filter_by(business_id=business.id).all()
    return render_template('products/manage.html', form=form, products=products, business=business)

@dashboard_bp.route('/products/update/<int:id>', methods=['POST'])
@csrf.exempt
@login_required
def update_product(id):
    product = Product.query.get_or_404(id)
    business = Business.query.get(product.business_id)
    if business.user_id != current_user.id:
        abort(403)
    
    product.name = request.form.get('name', product.name)
    product.price = request.form.get('price', product.price)
    
    if 'image' in request.files and request.files['image'].filename:
        img_path = save_uploaded_file(request.files['image'], 'products')
        if img_path:
            product.image = img_path
    
    db.session.commit()
    flash('Haryt täzelendi.', 'success')
    return redirect(request.referrer or url_for('dashboard.manage_products'))

@dashboard_bp.route('/products/delete/<int:id>', methods=['POST'])
@csrf.exempt
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    business = Business.query.get(product.business_id)
    if business.user_id != current_user.id:
        abort(403)
    db.session.delete(product)
    db.session.commit()
    flash('Haryt öçürildi.', 'success')
    return redirect(url_for('dashboard.manage_products'))

# Logo ýükle – CSRF exempt
@dashboard_bp.route('/business/logo/upload', methods=['POST'])
@csrf.exempt
@login_required
def upload_logo():
    business = Business.query.filter_by(user_id=current_user.id).first()
    if not business:
        abort(404)
    if 'logo' in request.files:
        file = request.files['logo']
        if file and file.filename:
            path = save_uploaded_file(file, 'logos')
            if path:
                business.logo = path
                db.session.commit()
                flash('Logo täzelendi.', 'success')
            else:
                flash('Logo ýüklemede ýalňyşlyk.', 'danger')
    return redirect(url_for('dashboard.index'))

# Cover ýükle – CSRF exempt
@dashboard_bp.route('/business/cover/upload', methods=['POST'])
@csrf.exempt
@login_required
def upload_cover():
    business = Business.query.filter_by(user_id=current_user.id).first()
    if not business:
        abort(404)
    if 'cover' in request.files:
        file = request.files['cover']
        if file and file.filename:
            path = save_uploaded_file(file, 'covers')
            if path:
                business.cover_image = path
                db.session.commit()
                flash('Cover suraty täzelendi.', 'success')
            else:
                flash('Cover ýüklemede ýalňyşlyk.', 'danger')
    return redirect(url_for('dashboard.index'))