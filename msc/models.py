from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import mapper, relationship
from werkzeug.security import generate_password_hash, \
     check_password_hash
from datetime import datetime
from msc.database import Base

def _get_date():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

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
    provider_id = Column(String(36), ForeignKey('providers.id'), nullable=True)
    created_at = Column(DateTime, nullable=False, default=_get_date)
    updated_at = Column(DateTime, nullable=False, default=_get_date, onupdate=_get_date)

    def __init__(self, uid=None, name=None, email=None, password=None, company=None, phone=None, address1=None, \
        address2=None, city=None, state=None, postal=None, country=None):
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
        self.provider_id = "e034baea-b649-4a6d-895f-da47b3f62619" #hardcode to Advantage     
        
    def __repr__(self):
        return 'User' + self.__dict__

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(String(36), primary_key=True)
    user = Column(String(36), ForeignKey(User.id),primary_key=True)
    customer_type = Column(SmallInteger, nullable=False)
    company_name = Column(String(120), nullable=False)
    contact_last_name = Column(String(120), nullable=False)    
    contact_first_name = Column(String(120), nullable=False)
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
    created_at = Column(DateTime, nullable=False, default=_get_date)
    updated_at = Column(DateTime, nullable=False, default=_get_date, onupdate=_get_date)

    def __init__(self, uid=None, user=None, customerType=None,  companyName=None, customerLastName=None, \
        customerFirstName=None, email=None, phone1=None, phone2=None, fax=None, website=None, \
        address1=None, address2=None, city=None, state=None, postal=None, country=None, \
        billAddress1=None, billAddress2=None, billCity=None, billState=None, billPostal=None, billCountry=None):
        self.id = uid
        self.user = user
        self.customer_type = customerType
        self.company_name = companyName
        self.contact_last_name = customerLastName
        self.contact_first_name = customerFirstName
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
        
    def __repr__(self):
        return 'Customer' + self.__dict__   

class Provider(Base):
    __tablename__ = 'providers'
    id = Column(String(36), primary_key=True)
    type = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(1024), nullable=False)
    members = relationship('User', backref='provider',
                                lazy='dynamic')
    created_at = Column(DateTime, nullable=False, default=_get_date)
    updated_at = Column(DateTime, nullable=False, default=_get_date, onupdate=_get_date)

    def __init__(self, uid=None, ttype=None, title=None, description=None):
        self.id = uid
        self.type = ttype
        self.title = title
        self.description = description     
        
    def __repr__(self):
        return 'Provider' + self.__dict__
     

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(String(36), primary_key=True)
    reporter = Column(String(36), ForeignKey(User.id), onupdate="cascade")
    provider = Column(String(36), ForeignKey(Provider.id), onupdate="cascade")
    type = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    pm_contract = Column(Integer, nullable=True)
    description = Column(String(1024), nullable=False)
    timeslot = Column(Integer, nullable=False)
    appointment_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=_get_date)
    updated_at = Column(DateTime, nullable=False, default=_get_date, onupdate=_get_date)

    def __init__(self, uid=None, reporter=None, ttype=None, quantity=None, pm_contract=None, description=None, timeslot=None, \
        appointment_at=None):
        self.id = uid
        self.reporter = reporter
        self.provider = "e034baea-b649-4a6d-895f-da47b3f62619" #hardcode to Advantage
        self.type = ttype
        self.quantity = quantity

        if pm_contract is not None and pm_contract == 'No':
            self.pm_contract = None
        else:
            self.pm_contract = pm_contract

        self.description = description
        self.timeslot = timeslot
        self.appointment_at = appointment_at     
        
    def __repr__(self):
        return 'Ticket' + self.__dict__
     