from sqlalchemy import String,Integer,Column,Float
from database import Base

class Ordenes(Base):
    __tablename__="ordenes"
    id_orden=Column(Integer, primary_key=True, index=True)
    nombre=Column(String(255))
    marca=Column(String(255))
    precio=Column(Float)
    cantidad=Column(Float)
    fecha=Column(String(255))
    