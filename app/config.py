import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # BASE_DIR - taslamaňyzyň kök papkasy
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Bazany göni kök papkada 'tmcard.db' hökmünde ýerleşdirýäris
    DB_PATH = os.path.join(BASE_DIR, 'tmcard.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload papkalary
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    LOGO_FOLDER = os.path.join(UPLOAD_FOLDER, 'logos')
    COVER_FOLDER = os.path.join(UPLOAD_FOLDER, 'covers')
    PRODUCT_FOLDER = os.path.join(UPLOAD_FOLDER, 'products')
    
    ADMIN_ID = 1
