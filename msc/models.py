from sqlalchemy import Column, Integer, String
from msc.database import Base
from werkzeug.security import generate_password_hash, \
     check_password_hash

class User(Base):
    __tablename__ = 'users'
    id = Column(String(32), primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(32), nullable=False))
    company = Column(String(120), nullable=False))
    phone = Column(String(32), nullable=False))
    address1 = Column(String(120), nullable=False))
    address2 = Column(String(120), nullable=False))
    city = Column(String(120), nullable=False))
    state = Column(String(120), nullable=False))
    postal = Column(String(32), nullable=False))
    country = Column(String(120), nullable=False))
    updated_at = Column(DateTime, nullable=False))

    def __init__(self, uuid, name, password, company, email, phone, address1, address2, city, state, postal, country):
        self.id = uuid
        self.name = name
        self.set_password(password)
        self.email = email
        self.phone = phone       
        

    def __repr__(self):
        return '<User %r>' % (self.name)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

def hashAPassword(userID, passToHash):

    me = User(userID, passToHash)
    hashedPassword = me.pw_hash

    print("hashedPassword--" , hashedPassword)

    return hashedPassword

