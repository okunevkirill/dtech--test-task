from datetime import datetime

from sqlalchemy import Column, Boolean, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String(128), unique=True)
    password = Column(String(255))
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    activate_hexdigest = Column(String(255))

    bills = relationship("Bill")
    rtoken = relationship("RefreshToken", uselist=False)

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"username={self.username}, is_superuser={self.is_superuser})")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    description = Column(String(255), default="")
    price = Column(Numeric(precision=10, scale=2), nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, price={self.price})"


class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    amount = Column(Numeric(precision=10, scale=2))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="bills")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, amount={self.amount})"


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    refresh_token = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="rtoken")
