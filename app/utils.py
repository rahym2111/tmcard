import qrcode
from io import BytesIO
import base64
import os
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def save_uploaded_file(file, subfolder):
    if not file or not file.filename:
        return None
    try:
        filename = secure_filename(file.filename)
        import uuid
        unique = str(uuid.uuid4())[:8] + '_' + filename
        folder = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, unique)
        file.save(filepath)
        # Return relative path for database
        return os.path.join('uploads', subfolder, unique).replace('\\', '/')
    except Exception as e:
        print(f"Upload error: {e}")
        return None