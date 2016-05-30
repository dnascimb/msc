from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://username:password@localhost/msc?charset=utf8', echo=True, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import msc.models
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    ####################################################
    # Create required database data
    ####################################################
    from msc.models import Provider, TicketType
    p = Provider("e034baea-b649-4a6d-895f-da47b3f62619", 1, "Advantage", "Advantage Fitness Equipment")
    db_session.add(p)
    ticket_type1 = TicketType("Multiple Services")
    ticket_type2 = TicketType("Elliptical Repair")
    ticket_type3 = TicketType("Elliptical Preventative Maintenance")
    ticket_type4 = TicketType("Cycle Repair")
    ticket_type5 = TicketType("Treadmill Repair")
    ticket_type6 = TicketType("Treadmill Preventative Maintenance")
    db_session.add(ticket_type1)
    db_session.add(ticket_type2)
    db_session.add(ticket_type3)
    db_session.add(ticket_type4)
    db_session.add(ticket_type5)
    db_session.add(ticket_type6)

    db_session.commit()

