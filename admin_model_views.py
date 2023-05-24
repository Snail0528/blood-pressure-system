"""后台管理视图"""
import os
from datetime import datetime

from flask import url_for, Markup, redirect
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import FileUploadField
from wtforms.validators import DataRequired
from wtforms.fields import StringField

from models import Users, db


class ImageUploadField(FileUploadField):
    def __init__(self, label=None, validators=None, base_path=None, relative_path=None, *args, **kwargs):
        super(ImageUploadField, self).__init__(label, validators, *args, **kwargs)
        self.base_path = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
        self.relative_path = 'static/uploads'


class UsersView(ModelView):
    column_list = [
        'username', 'email', 'avatar',
        'sig', 'created_at', 'is_admin',
    ]

    column_labels = {
        'username': '用户名',
        'password': '用户密码',
        'email': '用户邮箱',
        'avatar': '用户头像',
        'sig': '用户签名',
        'created_at': '注册时间',
        'is_admin': '是否为管理员'
    }
    
    column_descriptions = {
        'username': '请输入用户名',
        'password': '请输入密码',
        'email': '请输入邮箱地址',
        'avatar': '请上传头像',
        'sig': '请输入个性签名',
        'created_at': '注册时间',
        'is_admin': '是否为管理员（0: 不是，1: 是）'
    }
    
    form_args = {
        'username': {
            'label': '用户名',
            'description': '请输入用户名'
        },
        'password': {
            'label': '用户密码',
            'description': '请输入密码'
        },
        'email': {
            'label': '用户邮箱',
            'description': '请输入邮箱地址'
        },
        'avatar': {
            'label': '用户头像',
            'description': '请上传头像'
        },
        'sig': {
            'label': '用户签名',
            'description': '请输入个性签名'
        },
        'created_at': {
            'label': '注册时间',
            'description': '注册时间'
        },
        'is_admin': {
            'label': '是否为管理员',
            'description': '是否为管理员（0: 不是，1: 是）'
        }
    }
    form_overrides = dict(avatar=ImageUploadField)
    form_args = dict(
        avatar=dict(validators=[DataRequired()])
    )
    column_formatters = {
        'avatar': lambda v, c, m, p: Markup(f'<img src="{url_for("static", filename="uploads/" + (m.avatar if m.avatar else str("static/default.jpg")))}" height="40"/>')
    }


    def is_accessible(self):
        self.can_create = current_user.is_admin == '1' if current_user.is_authenticated else False
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

    def get_query(self):
        # 如果用户是管理员，则返回所有数据
        if current_user.is_admin == '1':
            return super().get_query()
        # 否则，只返回当前用户创建的数据
        return super().get_query().filter_by(id=current_user.id)

    def get_count_query(self):
        # 如果用户是管理员，则返回所有数据的数量
        if current_user.is_admin == '1':
            return super().get_count_query()
        # 否则，只返回当前用户创建的数据的数量
        return super().get_count_query().filter_by(id=current_user.id)

    def on_form_prefill(self, form, id):
        # 如果用户不是管理员，则限制可以编辑的字段
        if not current_user.is_admin == '1':
            # 将只读字段设置为不可编辑状态
            form.is_admin.data = form.is_admin.data
            del form.is_admin

        # 否则，允许编辑所有字段
        super().on_form_prefill(form, id)

class PatientImportView(ModelView):
    column_labels = {
        'id': '导入ID+用户ID',
        'export_id': '导入ID',
        'patient_name': '患者姓名',
        'gender': '患者性别',
        'age': '患者年龄',
        'height': '患者身高',
        'weight': '患者体重',
        'username': '用户姓名',
        'cate': '血压类型',
        'cluster': 'kmeans聚类预测患者血压',
    }

    column_descriptions = {
        'id': '导入记录的ID，同时包含用户ID',
        'export_id': '患者数据导入的时间戳',
    }

    column_list = ['patient_name', 'gender', 'age', 'height', 'weight', 'username', 'export_id', 'cluster', 'cate']
    column_sortable_list = ['id', 'patient_name', 'gender', 'age', 'height', 'weight', 'username', 'export_id', 'cluster', 'cate']
    column_searchable_list = ['patient_name', 'username']
    column_filters = ['gender', 'age', 'height', 'weight', 'cluster', 'cate']

    form_args = {
        'id': {'render_kw': {'readonly': True}},
        # 'username': {
        #     'label': '用户',
        #     'query_factory': lambda: db.session.query(username=Users.username).all(),
        #     'widget': 'select2',
        # },
    }

    form_widget_args = {
        'gender': {
            'placeholder': '请选择患者性别',
        },
        'age': {
            'placeholder': '请输入患者年龄',
        },
        'height': {
            'placeholder': '请输入患者身高',
        },
        'weight': {
            'placeholder': '请输入患者体重',
        },
    }

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

    def on_form_prefill(self, form, id):
        # 将只读字段设置为不可编辑状态
        form.username.data = current_user.username
        del form.username
        form.cluster.data = form.cluster.data
        del form.cluster
        form.cate.data = form.cate.data
        del form.cate


    column_formatters = {
        'export_id': lambda v, c, m, p: datetime.strftime(datetime.fromtimestamp(int(m.export_id)), '%Y-%m-%d %H:%M:%S'),
    }


class DashboardView(AdminIndexView):
    def is_visible(self):
        return False
