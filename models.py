from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from werkzeug.security import check_password_hash

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(100))
    sig = db.Column(db.String(100), default='')
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    is_admin = db.Column(db.Enum('0', '1'), nullable=False, default='0')

    def __repr__(self):
        return '<User %r>' % self.username

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.username

    def is_authenticated(self):
        # 如果用户已经通过 login_user() 函数登录并记住，则返回 True
        if current_user.is_authenticated and current_user.get_id() == str(self.id):
            return True
        else:
            return False


class PatientImport(db.Model):
    __tablename__ = 'patient_import'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    export_id = db.Column(db.String(50), nullable=False)
    patient_name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.Enum('男', '女'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    cate = db.Column(db.String(255), default='其他')
    cluster = db.Column(db.String(255), default='暂无分类')
    username = db.Column(db.String(50), db.ForeignKey('users.username'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('export_id', 'patient_name', name='_export_id_patient_name_uc'),
    )

    def __repr__(self):
        return '<PatientImport %r>' % self.id


class PatientData(db.Model):
    __tablename__ = 'patient_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    systolic = db.Column(db.Integer, nullable=False)
    diastolic = db.Column(db.Integer, nullable=False)
    heartrate = db.Column(db.Integer, nullable=False)
    ctime = db.Column(db.DateTime, nullable=False)
    export_id = db.Column(db.String(50), nullable=False)
    patient_name = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        db.ForeignKeyConstraint(['export_id', 'patient_name'],
                                 ['patient_import.export_id', 'patient_import.patient_name']),
    )

    def __repr__(self):
        return '<PatientData %r>' % self.id


class UserAnalysis(db.Model):
    analysis_id = db.Column(db.String(50), primary_key=True)
    analysis_data = db.Column(db.JSON)
    username = db.Column(db.String(50), db.ForeignKey('users.username'), nullable=False)
    export_id = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<UserAnalysis %r>' % self.analysis_id
