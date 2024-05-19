from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
from models import *
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
app.title="Ferremax"
app.version="0.0.1"


class IngresoProducto(BaseModel):
    nombre:str
    marca:str
    precio:float
    fecha:str

class ActualizarProducto(BaseModel):
    id_producto:int
    nombre:str
    marca:str
    precio:float
    fecha:str 

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/',tags=["Home"])
def home():
    return "Hola mundo"

@app.post("/producto/",status_code=status.HTTP_201_CREATED, tags=["Productos"])
async def crearProducto(producto:IngresoProducto, db:db_dependency):
    db_producto = Productos(**producto.dict())
    db.add(db_producto)
    db.commit()
    return "El producto se ha creado exitosamente"

@app.get("/producto/", status_code=status.HTTP_200_OK, tags=["Productos"])
async def listarProductos(db:db_dependency):
    productos= db.query(Productos).all()
    return productos

@app.get("/producto/{id}", status_code=status.HTTP_200_OK, tags=["Productos"])
async def listarProductoId(id, db:db_dependency):
    producto= db.query(Productos).filter(Productos.id_producto==id).first()
    if producto is None:
        HTTPException(status_code=404, detail="producto no encontrado")
        return "no encontrado"
    return producto   

@app.delete("/producto/{id}", status_code=status.HTTP_200_OK, tags=["Productos"])
async def eliminarProducto(id, db:db_dependency):
    producto = db.query(Productos).filter(Productos.id_producto== id).first()
    if producto is None:
        HTTPException(status_code=404, detail="producto no encontrado")
        return "no encontrado"
    db.delete(producto)
    db.commit()
    return "El producto se eliminó exitosamente"

@app.post("/producto/actualizar", status_code=status.HTTP_200_OK,tags=["Productos"])
async def actualizarProducto(producto:ActualizarProducto, db:db_dependency):
    act= db.query(Productos).filter(Productos.id_producto==producto.id_producto).first()
    if act is None:
        HTTPException(status_code=404, detail="producto no encontrado")
        return "no encontrado"
    
    act.id_producto=producto.id_producto
    act.nombre=producto.nombre
    act.marca=producto.marca
    act.precio=producto.precio
    act.fecha=producto.fecha
    db.commit()
    return "Producto actualizado exitosamente"
   
