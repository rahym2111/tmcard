import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Tuplyk açary
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # SQLite bazasynyň absolute ýoly (Windows üçin dogrulan)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, 'instance', 'tmcard.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{DB_PATH.replace(os.sep, "/")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Faýl ýükleme sazlamalary
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'app/static/uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    LOGO_FOLDER = os.path.join(UPLOAD_FOLDER, 'logos')
    COVER_FOLDER = os.path.join(UPLOAD_FOLDER, 'covers')
    PRODUCT_FOLDER = os.path.join(UPLOAD_FOLDER, 'products')
    
    # Admin hökmünde saýlanan ulanyjynyň ID-si (ilkinji hasap)
    ADMIN_ID = 1