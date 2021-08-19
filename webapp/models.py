from webapp import db, login_manager
from flask_login import UserMixin
from webapp import bcrypt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    history = db.relationship('Record', backref='owned_user', lazy=True)
    
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')    

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)   

class Record(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    start = db.Column(db.DateTime(timezone=True), nullable=False)
    end = db.Column(db.DateTime(timezone=True), nullable=False)
    note = db.Column(db.String(length=1024), nullable=True, unique=True)
    owner_user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    owner_ins = db.Column(db.Integer(), db.ForeignKey('instrument.id'))

class Instrument(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    ins_type = db.Column(db.String(length=100), nullable=False)
    ins_name = db.Column(db.String(length=30), nullable=False, unique=True)
    history =  db.relationship('Record', backref='owned_ins', lazy=True)
    note = db.Column(db.String(length=1024))
    cal_due = db.Column(db.DateTime(timezone=True))
    
    def __repr__(self):
        return f'Item {self.ins_name}'

    