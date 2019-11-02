from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

#def __init__(self, username, email, password):
#        self.username = username
#        self.email = email
#        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
        
class Index(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make_id = db.Column(db.Integer, db.ForeignKey('make.id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('modelyear.id'), nullable=False)
    trim_id = db.Column(db.Integer, db.ForeignKey('trim.id'), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    condition = db.Column(db.String(10), nullable=True)
    year = db.Column(db.Integer, nullable = False)
    fuel_type = db.Column(db.String(12), nullable=True)
    title = db.Column(db.String(12), nullable=True)
    fuel_type = db.Column(db.String(12), nullable=True)
    vin = db.Column(db.String(18), nullable=False)
    ext_color = db.Column(db.String(12), nullable=True)
    int_color = db.Column(db.String(12), nullable=True)
    body_type = db.Column(db.String(12), nullable=True)
    size = db.Column(db.String(12), nullable=True)
    drive = db.Column(db.String(12), nullable=True)
    engine = db.Column(db.String(20), nullable=True)
    url = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='vehicle.jpg')
    odo = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    warranty = db.Column(db.Boolean, nullable=True)
    dealer = db.Column(db.Boolean, nullable=True)
    automatic = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return f"Index('{self.year}', '{self.make_id}')"
    
class Make(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Index('{self.name}')"
    
    
class Modelyear(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=True)
    make_id = db.Column(db.Integer, db.ForeignKey('make.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f"Index('{self.name}')"
    
class Trim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('make.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f"Index('{self.name}')"
    
    
        
#todo:  ###  create db model for vehicles, vehicle index  #####




