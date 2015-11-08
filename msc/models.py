from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, ForeignKey
from msc.database import Base
from werkzeug.security import generate_password_hash, \
     check_password_hash

class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
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

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(String(36), primary_key=True)
    user = Column(String(36), ForeignKey(User.id),primary_key=True)
    type = Column(SmallInteger, nullable=False)
    name = Column(String(120), nullable=False)
    contact_name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone1 = Column(String(32), nullable=False)    
    phone2 = Column(String(32), nullable=True)
    fax = Column(String(32), nullable=True)
    website = Column(String(32), nullable=True)
    address1 = Column(String(120), nullable=False)
    address2 = Column(String(120), nullable=True)
    city = Column(String(120), nullable=False)
    state = Column(String(120), nullable=False)
    postal = Column(String(32), nullable=False)
    country = Column(String(120), nullable=False)
    bill_address1 = Column(String(120), nullable=False)
    bill_address2 = Column(String(120), nullable=True)
    bill_city = Column(String(120), nullable=False)
    bill_state = Column(String(120), nullable=False)
    bill_postal = Column(String(32), nullable=False)
    bill_country = Column(String(120), nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, uid=None, user=None, ctype=None, customerName=None, \
        contactName=None, email=None, phone1=None, phone2=None, fax=None, website=None, \
        address1=None, address2=None, city=None, state=None, postal=None, country=None, \
        billAddress1=None, billAddress2=None, billCity=None, billState=None, billPostal=None, billCountry=None, \
        updated_at=None):
        self.id = uid
        self.user = user
        self.type = ctype
        self.name = customerName
        self.contact_name = contactName
        self.email = email
        self.phone1 = phone1
        self.phone2 = phone2
        self.fax = fax
        self.website = website
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.postal = postal
        self.country = country
        self.bill_address1 = billAddress1
        self.bill_address2 = billAddress2
        self.bill_city = billCity
        self.bill_state = billState
        self.bill_postal = billPostal
        self.bill_country = billCountry
        self.updated_at = updated_at      
        
    def __repr__(self):
        return 'Customer' + self.__dict__
