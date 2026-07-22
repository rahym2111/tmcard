from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

# Ulanyjy modeli
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    businesses = db.relationship('Business', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Biznes modeli (indi views pole goşuldy)
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    logo = db.Column(db.String(255))
    cover_image = db.Column(db.String(255))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    phone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    email = db.Column(db.String(100))
    instagram = db.Column(db.String(100))
    tiktok = db.Column(db.String(100))
    telegram = db.Column(db.String(100))
    address = db.Column(db.String(255))
    maps_link = db.Column(db.String(255))
    opening_time = db.Column(db.String(10))
    closing_time = db.Column(db.String(10))
    views = db.Column(db.Integer, default=0)          # Görüş sany
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    products = db.relationship('Product', backref='business', lazy=True, cascade='all, delete-orphan')

# Haryt modeli
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255))
    price = db.Column(db.String(50))  # description aýryldy
    created_at = db.Column(db.DateTime, default=datetime.utcnow)