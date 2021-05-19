from flask import redirect, render_template
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import login_manager, login_user, current_user, logout_user

from TracyShopApp import admin, db, models
from TracyShopApp.models import *


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.is_authenticated:
            return True

        return False


class MyViewAdmin(BaseView):
    @expose('/')
    def index(self):
        return self.render()

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.user_role == UserRole.MANAGER or current_user.user_role == UserRole.STAFF:
            return True

        return False