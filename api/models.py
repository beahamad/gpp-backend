from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    confirmation_code = db.Column(db.String(4), nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    phones = db.relationship('Phone', backref='user', lazy=True)

class Phone(db.Model):
    __tablename__ = 'phone'

    id = db.Column(db.Integer, primary_key=True)
    imei = db.Column(db.String(15), unique=True, nullable=False)
    number1 = db.Column(db.String(20), unique=True, nullable=False)
    number2 = db.Column(db.String(20), unique=True, nullable=False)
    is_lost = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
