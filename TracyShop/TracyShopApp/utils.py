from TracyShopApp.models import *
import hashlib


#Kiểm tra xem có phải là Manager không
def check_manager(username, password, role=UserRole.MANAGER):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User.query.filter(User.username == username,
                             User.password == password,
                             User.userRole == role).first()
    return user


#Kiểm tra xem có phải là Staff không
def check_staff(username, password, role=UserRole.STAFF):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User.query.filter(User.username == username,
                             User.password == password,
                             User.userRole == role).first()
    return user


#Kiểm tra xem có phải là Customer không
def check_customer(username, password, role=UserRole.CUSTOMER):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User.query.filter(User.username == username,
                             User.password == password,
                             User.userRole == role).first()
    return user


#Thêm địa chỉ
def add_address(road, ward, district, city):
    address = Address(road, ward, district, city)
    try:
        db.session.add(address)
        db.session.commit()
        return address
    except:
        return False


#đăng ký tài khoản người dùng
def register_user(name, phone, gender, birthday, username, password, avatar, active, user_role, road, ward, district, city):
    address = add_address(road=road, ward=ward, district=district, city=city)
    password = str(hashlib.md5(password.trip().encode('utf-8')).hexdigest())
    user = User(name=name,
                phone=phone,
                gender=gender,
                birtday=birthday,
                username=username,
                password=password,
                avatar=avatar,
                active=active,
                user_role=user_role,
                addressId=Address.id)
    try:
        db.session.add(user)
        db.session.commit()
        return True
    except:
        return False


#tạo khách hàng kết nối đến user
def create_customer(user_id):
    customer = Customer(user_id)
    try:
        db.session.add(customer)
        db.session.commit()
        return True
    except:
        return False


#tạo nhân viên kết nối đến user
def create_staff(user_id):
    staff = Staff(user_id)
    try:
        db.session.add(staff)
        db.session.commit()
        return True
    except:
        return False


#kiểm tra username có trùng hay không
def check_username(username):
    user = User.query.all() # cái câu query này bn viết đúng chưa ak, hya là db.query ? đúng r í
    for u in user:
        if u.username == username:
            return True
        return False


#lấy id của người dùng
def get_id_user(username=None):
    user = User.query.all()
    for u in user:
        if u.username == username:
            return u.id


#Lấy tài khoản người dùng bằng id
def get_user_by_id(user_id):
    return User.query.get(user_id)


#tạo đơn hàng mới
def create_order(customer_id, address, is_pay, staff_id):
    order = Order(date=datetime.today(),
                  isCensorship=False,
                  isPay=is_pay,
                  paymentMenthodId=1,
                  staffId=staff_id,
                  totalBill=0)
    try:
        db.session.add(order)
        db.session.commit()
        return True
    except:
        return False









