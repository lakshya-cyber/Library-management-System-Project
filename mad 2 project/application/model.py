from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime
db = SQLAlchemy()


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    Name = db.Column(db.String(120))
    email = db.Column(db.String(120),  nullable=False)
    password = db.Column(db.String(60), nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True)
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))
    active = db.Column(db.Boolean(), default=True)
    approvals = db.relationship('Approval', backref='user')
    requests = db.relationship('Request_books',backref = 'user')

    

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Section(db.Model):
    section_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False,unique = True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    description = db.Column(db.Text)
    books = db.relationship('Book', backref=db.backref('section'))



class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300))
    authors = db.Column(db.String(100))
    section_id = db.Column(db.Integer, db.ForeignKey('section.section_id'),nullable=False)
    approvals = db.relationship('Approval', backref='book')
    requests = db.relationship('Request_books',backref = 'book')
    feedbacks = db.relationship('Feedback', backref=db.backref('book'))

    

class Request_books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))
    book_name = db.Column(db.String(100))
    user_email = db.Column(db.String(100), db.ForeignKey('user.email'))
    days_requested = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    date_issued = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    


class Approval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100))
    book_id =db.Column(db.Integer, db.ForeignKey('book.book_id'))
    book_author = db.Column(db.String(100))
    book_content = db.Column(db.String(300))
    section_id = db.Column(db.Integer, db.ForeignKey('section.section_id'))
    user_email = db.Column(db.String(100), db.ForeignKey('user.email')) 

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))


