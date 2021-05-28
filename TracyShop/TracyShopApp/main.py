from TracyShopApp import app, login
from flask import render_template
from TracyShopApp.admin import *


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
            err_msg = "Username or password incorrect"

    return render_template('login.html', err_msg=err_msg)


if __name__ == "__main__":
    app.run(debug=True)