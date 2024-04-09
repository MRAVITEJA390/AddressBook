from sqlalchemy import Column, Float, Integer, String

from database import Base


class AddressBook(Base):
    __tablename__ = "addressbook"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
