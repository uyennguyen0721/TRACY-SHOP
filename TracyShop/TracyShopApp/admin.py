from flask import redirect, render_template, request
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import login_manager, login_user, current_user, logout_user

from TracyShopApp import admin, db, models, utils
from TracyShopApp.models import *


#Đăng xuất
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


#trang admin
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


# ****** dành cho manager và staff ******




# ****** chỉ dành riêng cho manager ******

#xem thông tin nhân viên
class ViewStaff(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def view_staff(self):
        err_msg = ""
        user = db.session.query(User).filter(User.id == Staff.userId)
        staff = db.session.query(Staff).all()
        address = db.session.query(Address).all()
        return self.render('admin/view-staff-informations.html', err_msg=err_msg, user=user, staff=staff, address=address)

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.user_role == UserRole.MANAGER:
            return True

        return False


#thêm nhân viên
class AddStaff(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def add_staff(self):
        err_msg = ""
        if request.menthod == 'POST':
            name = request.form.get('name')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm-password')
            if password == confirm_password:
                username = request.form.get('username')
                gender = request.form.get('gender')
                phone = request.form.get('phone')
                birthday = request.form.get('birthday')
                road = request.form.get('road')
                ward = request.form.get('ward')
                district = request.form.get('district')
                city = request.form.get('city')
                avatar_path = 'image/upload/abc.jpg'
                if utils.check_username(username=username):
                    err_msg = "This username already exists. Please use another name!"
                elif utils.register_user(name=name, phone=phone, gender=gender, birthday=birthday, username=username, password=password, avatar=avatar_path, active=1, user_role=UserRole.STAFF, road=road, ward=ward, district=district, city=city):
                    u = utils.get_id_user(username)
                    utils.create_staff(u)
                    err_msg = "Account created successfully!"
            else:
                err_msg = "Confirm password is not correct. Please check again!"
        return self.render('admin/add-staff.html', err_msg=err_msg)

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.user_role == UserRole.MANAGER:
            return True

        return False




