from TracyShopApp.models import *
import hashlib


#Kiểm tra xem có phải là Manager không
def checkManager(username, password, role=UserRole.MANAGER):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User.query.filter(User.username == username,
                             User.password == password,
                             User.userRole == role).first()
    return user


#Kiểm tra xem có phải là Staff không
def checkStaff(username, password, role=UserRole.STAFF):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User.query.filter(User.username == username,
                             User.password == password,
                             User.userRole == role).first()
    return user


#Kiểm tra xem có phải là Customer không
def checkCustomer(username, password, role=UserRole.CUSTOMER):
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


#đăng ký tài khoản người dùng khách hàng
def register_customer(name, phone, gender, birtday, username, password, avatar, active, user_role, road, ward, district, city):
    address = add_address(road=road, ward=ward, district=district, city=city)
    password = str(hashlib.md5(password.trip().encode('utf-8')).hexdigest())
    user = User(name=name,
                phone=phone,
                gender=gender,
                birtday=birtday,
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








