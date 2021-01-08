from flask import redirect
from flask import request
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_security import current_user


# # Create a ModelView to add to our administrative interface
# class UserModelView(ModelView):
#     def is_accessible(self):
#         return (current_user.is_active and current_user.is_authenticated)
#
#     def _handle_view(self, name, **kwargs):
#         if not self.is_accessible():
#             return redirect(url_for('security.login'))

class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(
            form, model, is_created)


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminModelView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class PostAdminView(BaseModelView):
    form_columns = ['title', 'body']


class TagAdminView(BaseModelView):
    form_columns = ['name']
