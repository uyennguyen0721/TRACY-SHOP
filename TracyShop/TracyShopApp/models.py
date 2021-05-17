from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, \
    Boolean, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from TracyShopApp import db
from flask_login import UserMixin
import enum


class SaleBase(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class UserRole(enum.Enum):
    MANAGER = 1
    STAFF = 2
    CUSTOMER = 3

    def __str__(self):
        return self.name


class Address(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    road = Column(String(100), nullable=False)
    ward = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    phone = Column(String(100))
    gender = Column(String(100))
    birthday = Column(DateTime)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    joinedDate = Column(DateTime, default=datetime.today())
    userRole = Column(Enum(UserRole), default=UserRole.CUSTOMER)

    addressId = Column(Integer, ForeignKey(Address.id), nullable=False)
    staffProfiles = db.relationship('Staff', uselist=False, back_populates="user")
    customerProfiles = db.relationship('Customer', uselist=False, back_populates="user")


class Staff(db.Model):

    userId = Column(Integer, ForeignKey(User.id), primary_key=True)
    orders = relationship('Order', backref="staff", lazy=True)
    users = db.relationship('User', back_populates='staffProfiles')


class Customer(User):

    orders = relationship('Order', backref="customer", lazy=True)
    userId = db.Column(Integer, ForeignKey(User.id), primary_key=True)
    users = db.relationship('User', back_populates='customerProfiles', uselist=False)


class PaymentMethod(SaleBase):

    __tablename__ = "paymentmethod"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    orders = relationship('Order', backref="paymentmethod", lazy=True)


class Order(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    isCensorship = Column(Boolean, nullable=False)
    isPay = Column(Boolean, nullable=False)
    totalBill = Column(Float, nullable=False)

    staffId = Column(Integer, ForeignKey(Staff.userId), nullable=False)
    customerId = Column(Integer, ForeignKey(Customer.userId), nullable=False)
    paymentMethodId = Column(Integer, ForeignKey(PaymentMethod.id), nullable=False)

    orderDetails = relationship('OrderDetail', back_populates="Order")


class Category(SaleBase):
    products = relationship('Product', backref="Category", lazy=True)


class Product(SaleBase):
    description = Column(String(100), nullable=True)
    price = Column(Float, nullable=False)
    image = Column(String(100), nullable=True)
    quantity = Column(Integer, nullable=False)

    categoryId = Column(Integer, ForeignKey(Category.id), nullable=False)

    orderDetails = relationship('OrderDetail', back_populates="Order")


class OrderDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
    unitPrice = Column(Float, nullable=False)

    orderId = Column(Integer, ForeignKey(Order.id), nullable=False)
    productId = Column(Integer, ForeignKey(Product.id), nullable=False)


if __name__ == "__main__":
    db.create_all()