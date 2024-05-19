from sqlalchemy import String,Integer,Column,Float
from database import Base

class Productos(Base):
    __tablename__="productos"
    id_producto=Column(Integer, primary_key=True, index=True)
    nombre=Column(String(255))
    marca=Column(String(255))
    precio=Column(Float)
    fecha=Column(String(255))
    