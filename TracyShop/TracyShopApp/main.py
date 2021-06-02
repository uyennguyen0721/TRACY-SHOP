from TracyShopApp import app, login
from flask import render_template, url_for
from TracyShopApp.admin import *


#trang chủ
@app.route("/")
def index():
    return render_template("index.html")


#đăng nhập
@login.user_loader
def get_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    err_msg = ""

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')
        customer = utils.check_customer(username=username, password=password)
        manager = utils.check_manager(username=username, password=password)
        staff = utils.check_staff(username=username, password=password)
        if customer:
            login_user(user=customer)
            return redirect("/")
        elif manager:
            login_user(user=manager)
            return redirect("/admin")
        elif staff:
            login_user(user=staff)
            return redirect("/admin")
        else:
            err_msg = "Tên đăng nhập hoặc mật khẩu chưa đúng"

    return render_template('login.html', err_msg=err_msg)


#đăng ký
@app.route('/register', methods=['GET', 'POST'])
def register():
    err_msg = ""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm-password')
        if password == confirm:
            name = request.form.get('name')
            phone = request.form.get('phone')
            username = request.form.get('username')
            birthday = request.form.get('birthday')
            gender = request.form.get('gender')
            avatar_path = 'static/images/default-avatar.png'
            if utils.check_username(username):
                err_msg = "Tên đăng nhập đã được sử dụng"
            elif utils.register_user(name=name, phone=phone, gender=gender, birthday=birthday, username=username,
                                     password=password, avatar=avatar_path, active=1, user_role=utils.UserRole.CUSTOMER,
                                     road="371 Nguyễn Kiệm", ward="phường 7", district="quận Gò Vấp", city="Hồ Chí Minh"):
                user = utils.get_id_user(username)
                utils.check_customer(user)
                err_msg = "Tạo tài khoản thành công"
        else:
            err_msg = "Mật khẩu không khớp vui lòng thử lại"

    return render_template('register.html', err_msg=err_msg)


#đăng xuất
@app.route('/logout')
def logout_usr():
    logout_user()
    return redirect(url_for('index'))


#trang Về Tracy Shop
@app.route('/about-us')
def about_us():
    return render_template('about-us.html')


if __name__ == "__main__":
    app.run(debug=True)