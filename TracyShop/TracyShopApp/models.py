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
    ADMIN = 1
    NHANVIEN = 2
    KHACHHANG = 3

    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    diachi = Column(String(100), nullable=False)
    sdt = Column(String(100))
    gioitinh = Column(String(100))
    ngaysinh = Column(DateTime)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    ngaytg = Column(DateTime, default=datetime.today())
    user_role = Column(Enum(UserRole), default=UserRole.KHACHHANG)
    nhanvien_profiles = db.relationship('NhanVien', uselist=False, back_populates="user")
    khachhang_profiles = db.relationship('KhachHang', uselist=False, back_populates="user")


class NhanVien(db.Model):
    __tablename__ = 'nhanvien'

    cmnd = Column(String(100))
    id = Column(Integer, primary_key=True, autoincrement=True)
    # the one-to-one relation
    user_id = db.Column(Integer, ForeignKey('user.id'))
    donhang = relationship('DonHang', backref="nhanvien", lazy=True)
    user = db.relationship('User', back_populates='nhanvien_profiles')
    khachang = relationship("GhiNo", back_populates="nhanvien")


class KhachHang(db.Model):
    __tablename__ = 'khachhang'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # the one-to-one relation
    user_id = db.Column(Integer, ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', back_populates='khachhang_profiles', uselist=False)
    donhang = relationship('DonHang', backref="khachang", lazy=True)
    nhanvien = relationship("GhiNo", back_populates="khachhang")
