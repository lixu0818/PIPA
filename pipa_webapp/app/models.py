# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func

from app import db, login_manager

class User(UserMixin, db.Model):
    """
    Create a User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    created = db.Column(db.DateTime(timezone=True), default=db.func.now())
    lastmodified = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class UserArticle(db.Model):
    """
    Create a user_articles table
    """

    __tablename__ = 'user_articles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pmid = db.Column(db.Integer)
    title = db.Column(db.String(200))
    abstract = db.Column(db.String(1000))
    created = db.Column(db.DateTime(timezone=True), default=func.now())
    lastmodified = db.Column(db.DateTime(timezone=True), onupdate=func.now())  
    deleted = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return '<UserArticle: {}>'.format(self.id)


class RecommendArticle(db.Model):
    """
    Create a recommend_articles table
    """

    __tablename__ = 'user_articles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    source_pmid = db.Column(db.Integer, db.ForeignKey('user_articles.pmid'))
    entry_date = db.Column(db.DateTime(timezone=True))
    pmid_1 = db.Column(db.Integer)
    pmid_2 = db.Column(db.Integer)
    pmid_3 = db.Column(db.Integer)
    pmid_4 = db.Column(db.Integer)
    pmid_5 = db.Column(db.Integer)
    pmid_6 = db.Column(db.Integer)
    pmid_7 = db.Column(db.Integer)
    pmid_8 = db.Column(db.Integer)
    pmid_9 = db.Column(db.Integer)
    pmid_10 = db.Column(db.Integer)
    score_1 = db.Column(db.Float)
    score_2 = db.Column(db.Float)
    score_3 = db.Column(db.Float)
    score_4 = db.Column(db.Float)
    score_5 = db.Column(db.Float)
    score_6 = db.Column(db.Float)
    score_7 = db.Column(db.Float)
    score_8 = db.Column(db.Float)
    score_9 = db.Column(db.Float)
    score_10 = db.Column(db.Float)

    def __repr__(self):
        return '<RecommendArticle: {}>'.format(self.id)





