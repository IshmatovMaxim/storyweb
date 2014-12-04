from flask import g, redirect, url_for, request
from wtforms import PasswordField
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from storyweb.core import app, db, app_name
from storyweb.model import User, Block


class AppModelView(ModelView):
    
    def is_accessible(self):
        if g.user is None:
            return False
        if not g.user.is_active():
            return False
        if not g.user.is_admin:
            return False
        return True

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))


class UserAdmin(AppModelView):
    column_list = [
        'email',
        'display_name',
        'active',
        'is_admin',
        'is_editor'
    ]
    column_exclude_list = ['password_hash']

    form_excluded_columns = [
        'password_hash',
        'blocks',
        'created_at',
        'updated_at',
        'active'
    ]

    column_labels = {
        'email': 'E-Mail',
        'is_admin': 'Administrator',
        'is_editor': 'Editor',
        'display_name': 'Name'
    }

    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password = PasswordField('Password')
        return form_class

    def on_model_change(self, form, model, is_created):
        model.password = form.password.data


class BlockAdmin(AppModelView):
    column_list = [
        'text',
        'source_label',
        'date'
    ]
    
    form_excluded_columns = [
        'references',
        'created_at',
        'updated_at'
    ]

    column_labels = {
        'text': 'Snippet',
        'source_label': 'Source',
        'source_url': 'Source link'
    }

    def on_model_change(self, form, model, is_created):
        pass


admin = Admin(app, name=app_name)
admin.add_view(UserAdmin(User, db.session))
admin.add_view(BlockAdmin(Block, db.session))
