from schemas.proveedor import Proveedor, UpdateProveedor, CreateProveedorIn, CreateProveedorOut
from models.models import ProveedorDB
from methods.cnx import SessionLocal
from uuid import uuid4

# Funcion que nos muestra todos los Proveedores
def getProveedores(activo=True):
    try:
        db = SessionLocal()
        proveedores = db.query(ProveedorDB).filter(ProveedorDB.activo == activo).all()
        if proveedores:
            db.close()
            return proveedores
        return None
    except Exception as e:
        raise e
    finally:
        db.close()

# Function to get one task
def getProveedorDB(id: str):
    try:
        db = SessionLocal()
        proveedor = db.query(ProveedorDB).filter(ProveedorDB.id == id).first()
        if proveedor:
            db.close()
            return proveedor
        return None
    except Exception as e:
        raise e                   
    
# Creation of "proveedor" is used in the "POST" method
def createProveedorDB(proveedor: CreateProveedorIn):
    try:
        db = SessionLocal()
        new_proveedor = ProveedorDB(
                        id=str(uuid4()),
                        cuit=proveedor.cuit,
                        nombre=proveedor.nombre,
                        direccion=proveedor.direccion, 
                        ciudad=proveedor.ciudad, 
                        telefono=proveedor.telefono, 
                        email=proveedor.email, 
                        sitio=proveedor.sitio
                    )
        db.add(new_proveedor)
        db.commit()
        db.refresh(new_proveedor)
        return new_proveedor
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close_all()

# Function to get update the "proveedor" is used in "PUT" methods
def updateProveedorDB(id: str, updated_proveedor: UpdateProveedor):
    try:
        db = SessionLocal()
        proveedor = db.query(ProveedorDB).filter(ProveedorDB.id == id).first()
        print(proveedor)
        if proveedor:
            proveedor.cuit=updated_proveedor.cuit
            proveedor.nombre=updated_proveedor.nombre
            proveedor.direccion=updated_proveedor.direccion
            proveedor.ciudad=updated_proveedor.ciudad
            proveedor.telefono=updated_proveedor.telefono
            proveedor.email=updated_proveedor.email
            proveedor.sitio=updated_proveedor.sitio
            db.commit()
            db.refresh(proveedor)
            return proveedor
        return None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Function to remove a "proveedor" by their ID, mode logical
def deleteProveedorDB(id: str):
    try:
        db = SessionLocal()
        proveedor = db.query(ProveedorDB).filter(ProveedorDB.id == id).first()
        if proveedor:
            proveedor.activo = False
            db.commit()
            db.refresh(proveedor)
        db.close()
        return proveedor
    except Exception as e:
        raise e
    finally:
        db.close()
