from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, EmailField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

# Hasaba alyş formy
class RegistrationForm(FlaskForm):
    name = StringField('Adyňyz', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Parol', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Paroly tassykla', validators=[DataRequired(), EqualTo('password')])
    business_name = StringField('Biznesiň ady', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Hasap döret')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Bu email eýýäm hasaba alyndy.')

# Giriş formy
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Parol', validators=[DataRequired()])
    submit = SubmitField('Giriş')

# Admin giriş formy
class AdminLoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Parol', validators=[DataRequired()])
    submit = SubmitField('Admin girişi')

# Biznes formy – bu ýerde TextAreaField gerek
class BusinessForm(FlaskForm):
    name = StringField('Biznes ady', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Kategoriýa', choices=[
        ('Restoran', 'Restoran'), ('Kafe', 'Kafe'), ('Magazin', 'Magazin'),
        ('Gözellik', 'Gözellik salon'), ('Hyzmat', 'Hyzmat'), ('Beýleki', 'Beýleki')
    ], validators=[DataRequired()])
    description = TextAreaField('Gysga düşündiriş')  # biznes üçin düşündiriş gerek
    phone = StringField('Telefon', validators=[Length(max=20)])
    whatsapp = StringField('WhatsApp', validators=[Length(max=20)])
    email = EmailField('Email', validators=[Email(), Length(max=100)])
    instagram = StringField('Instagram', validators=[Length(max=100)])
    tiktok = StringField('TikTok', validators=[Length(max=100)])
    telegram = StringField('Telegram', validators=[Length(max=100)])
    address = StringField('Adres', validators=[Length(max=255)])
    maps_link = StringField('Google Maps link', validators=[Length(max=255)])
    opening_time = StringField('Açylyş wagty', validators=[Length(max=10)])
    closing_time = StringField('Ýapylyş wagty', validators=[Length(max=10)])
    submit = SubmitField('Sakla')

# Haryt formy – düşündiriş aýryldy
class ProductForm(FlaskForm):
    name = StringField('Harydyň ady', validators=[DataRequired(), Length(max=100)])
    price = StringField('Bahasy', validators=[Length(max=50)])
    image = FileField('Surat', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Diňe surat faýllary')])
    submit = SubmitField('Goş')