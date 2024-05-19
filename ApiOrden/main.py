from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
from models import *
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
app.title="Ferremax"
app.version="0.0.1"


class IngresoOrden(BaseModel):
    nombre:str
    marca:str
    precio:float
    cantidad:float
    fecha:str

class ActualizarOrden(BaseModel):
    id_orden:int
    nombre:str
    marca:str
    precio:float
    cantidad:float
    fecha:str 

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/',tags=["Integración"])
def home():
    
    return "Hola integración"

@app.post("/orden/",status_code=status.HTTP_201_CREATED, tags=["Ordenes"])
async def crear_Orden(orden:IngresoOrden, db:db_dependency):
    db_orden = Ordenes(**orden.dict())
    db.add(db_orden)
    db.commit()
    return "La orden se ha creado exitosamente"

@app.get("/orden/", status_code=status.HTTP_200_OK, tags=["Ordenes"])
async def listar_Ordenes(db:db_dependency):
    ordenes= db.query(Ordenes).all()
    return ordenes

@app.get("/orden/{id}", status_code=status.HTTP_200_OK, tags=["Ordenes"])
async def listar_Orden_Id(id, db:db_dependency):
    orden= db.query(Ordenes).filter(Ordenes.id_orden==id).first()
    if orden is None:
        HTTPException(status_code=404, detail="orden no encontrada")
        return "no encontrado"
    return orden   

@app.delete("/orden/{id}", status_code=status.HTTP_200_OK, tags=["Ordenes"])
async def eliminar_Orden(id, db:db_dependency):
    orden = db.query(Ordenes).filter(Ordenes.id_orden== id).first()
    if orden is None:
        HTTPException(status_code=404, detail="orden no encontrada")
        return "no encontrado"
    db.delete(orden)
    db.commit()
    return "La orden se eliminó exitosamente"

@app.post("/orden/actualizar", status_code=status.HTTP_200_OK,tags=["Ordenes"])
async def actualizar_Orden(orden:ActualizarOrden, db:db_dependency):
    act= db.query(Ordenes).filter(Ordenes.id_orden==orden.id_orden).first()
    if act is None:
        HTTPException(status_code=404, detail="orden no encontrada")
        return "no encontrado"
    
    act.id_orden=orden.id_orden
    act.nombre=orden.nombre
    act.marca=orden.marca
    act.precio=orden.precio
    act.fecha=orden.fecha
    db.commit()
    return "Orden actualizado exitosamente"
   
