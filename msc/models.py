from sqlalchemy import Column, Integer, String, DateTime
from msc.database import Base
from werkzeug.security import generate_password_hash, \
     check_password_hash

class User(Base):
    __tablename__ = 'users'
    id = Column(String(32), primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(32), nullable=False)
    company = Column(String(120), nullable=False)
    phone = Column(String(32), nullable=False)
    address1 = Column(String(120), nullable=False)
    address2 = Column(String(120), nullable=False)
    city = Column(String(120), nullable=False)
    state = Column(String(120), nullable=False)
    postal = Column(String(32), nullable=False)
    country = Column(String(120), nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, uid=None, name=None, email=None, password=None, company=None, phone=None, address1=None, \
        address2=None, city=None, state=None, postal=None, country=None, updated_at=None):
        self.id = uid
        self.name = name
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        else:
            self.password = password
        self.company = company
        self.phone = phone
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.postal = postal
        self.country = country
        self.updated_at = updated_at      
        
    def __repr__(self):
        return 'User' + self.__dict__

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

