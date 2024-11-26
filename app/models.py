from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import IPAddressType
from enum import Enum as pyEnum
from . import db

# db = SQLAlchemy()

class gender(pyEnum):
    MALE = "male"
    FEMALE = "female"

class role(pyEnum):
    INTERVIEWER = "interviewer"
    INTERVIEWEE = "interviewee"

class User(db.Model):
    idUser = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.Enum(gender), nullable=True)
    role = db.Column(db.Enum(role), nullable=False)
    ip = db.Column(IPAddressType)

class self_introduction(db.Model):
    idIntro = db.Column(db.Integer, primary_key=True)
    detail = db.Column(db.Text(), nullable=True)
    uploaded = db.Column(db.DateTime(), nullable=True)
    suitable = db.Column(db.Boolean, nullable=True)

    # User의 idUser과 연결
    user_id = db.Column(db.Integer, db.ForeignKey('User.idUser', ondelete='CASCADE'), nullable=False)  # 외래 키
    # user과의 관계 설정 - User 1개에 여러 introduction이 있음 -> User객체.Introductions으로 User의 자소서 참조
    user = db.relationship("User", backref=db.backref('Introductions', cascade='all, delete-orphan'))
    # cascade='all, delete-orphan' -> User삭제할 때 자소서도 삭제됨

    ip = db.Column(IPAddressType)

class interview(db.Model):
    idInterview = db.Column(db.Integer, primary_key=True)
    dialog = db.Column(db.Text(), nullable=True)
    feedback = db.Column(db.Text(), nullable=True)
    date = db.Column(db.DateTime(), nullable=True)
    question = db.Column(db.Text(), nullable=True)

    # self_introduction과의 idIntro 연결
    intro_id = db.Column(db.Integer, db.ForeignKey('self_introduction.idIntro', ondelete='CASCADE'), nullable=False)  # 외래 키
    # self_introduction과의 관계 설정 - self_introduction과의 1개에 여러 interview가 있음 -> self_introduction객체.idIntro으로 self_introduction의 면접 참조
    self_introduction = db.relationship("self_introduction", backref=db.backref('Interviews', cascade='all, delete-orphan'))
    # cascade='all, delete-orphan' -> 자소서 삭제할 때 면접 기록도 삭제됨

    ip = db.Column(IPAddressType)
