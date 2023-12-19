from schemas.permiso import Permiso, UpdatePermiso, CreatePermisoIn, CreatePermisoOut
from models.models import PermisoDB
from methods.cnx import SessionLocal
from uuid import uuid4


def getPermisos(activo=True):
    try:
        db = SessionLocal()
        permisos = db.query(PermisoDB).filter(PermisoDB.activo == activo).all()
        if permisos:
            db.close()
            return permisos
        return None
    except Exception as e:
        raise e
    finally:
        db.close()

# Function to get one task
def getPermisoDB(id: str):
    try:
        db = SessionLocal()
        permiso = db.query(PermisoDB).filter(PermisoDB.id == id).first()
        if permiso:
            db.close()
            return permiso
        return None
    except Exception as e:
        raise e                   
    
# Creation of "permiso" is used in the "POST" method
def createPermisoDB(permiso: CreatePermisoIn):
    try:
        db = SessionLocal()
        new_permiso = PermisoDB(
                        id=str(uuid4()),
                        nombre=permiso.nombre,
                        tipo=permiso.tipo,
                        )    
        db.add(new_permiso)
        db.commit()
        db.refresh(new_permiso)
        return new_permiso
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close_all()

# Function to get update the "permiso" is used in "PUT" methods
def updatePermisoDB(id: str, updated_permiso: UpdatePermiso):
    try:
        db = SessionLocal()
        permiso = db.query(PermisoDB).filter(PermisoDB.id == id).first()
        print(permiso)
        if permiso:            
            permiso.nombre=updated_permiso.nombre
            permiso.tipo=updated_permiso.tipo
            db.commit()
            db.refresh(permiso)
            return permiso
        return None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Function to remove a "permiso" by their ID, mode logical
def deletePermisoDB(id: str):
    try:
        db = SessionLocal()
        permiso = db.query(PermisoDB).filter(PermisoDB.id == id).first()
        if permiso:
            permiso.activo = False
            db.commit()
            db.refresh(permiso)
        db.close()
        return permiso
    except Exception as e:
        raise e
    finally:
        db.close()
