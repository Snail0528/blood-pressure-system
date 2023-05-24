from flask import Flask
from flask_admin import Admin
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_babelex import Babel
from flask_session import Session
from sqlalchemy.engine.reflection import Inspector

import views
from models import Users, PatientImport, db
from admin_model_views import UsersView, PatientImportView, DashboardView


#flask框架
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='')
app.secret_key = 'custom123897'
app.config['DEBUG'] = True
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/blood_pressure'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_REMEMBER'] = True

db.init_app(app)
babel = Babel(app)
photos = UploadSet('photos', IMAGES)
views.login_manager.init_app(app)
session = Session(app)
configure_uploads(app, photos)

admin = Admin(app, name='血压数据后台管理系统', template_mode='bootstrap4', index_view=DashboardView(), url='/')
admin.add_view(UsersView(Users, db.session, '用户表'))
admin.add_view(PatientImportView(PatientImport, db.session, '患者导入表'))
app.register_blueprint(views.bp)

@app.before_request
def init():
    inspector = Inspector.from_engine(db.engine)
    tables = [x.name for x in db.get_tables_for_bind()]
    for t in tables:
        if t not in inspector.get_table_names():
            db.create_all()
            break

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888)
