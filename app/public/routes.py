from flask import Blueprint, render_template
from app.models import Business

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    return render_template('index.html')