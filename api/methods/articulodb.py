from schemas.articulo import Articulo, UpdateArticulo, CreateArticuloIn, CreateArticuloOut
from models.models import ArticuloDB
from methods.cnx import SessionLocal
from uuid import uuid4

# Funcion que nos muestra todos los Articuloes
def getArticulos(activo=True):
    try:
        db = SessionLocal()
        articulos = db.query(ArticuloDB).filter(ArticuloDB.activo == activo).all()
        if articulos:
            db.close()
            return articulos
        return None
    except Exception as e:
        raise e
    finally:
        db.close()

# Function to get one task
def getArticuloDB(id: str):
    try:
        db = SessionLocal()
        articulo = db.query(ArticuloDB).filter(ArticuloDB.id == id).first()
        if articulo:
            db.close()
            return articulo
        return None
    except Exception as e:
        raise e                   
    
# Creation of "articulo" is used in the "POST" method
def createArticuloDB(articulo: CreateArticuloIn):
    try:
        db = SessionLocal()
        new_articulo = ArticuloDB(
                        id=str(uuid4()),
                        nombre=articulo.nombre,
                        tipo=articulo.tipo, 
                        marca=articulo.marca,
                        modelo=articulo.modelo,
                        anio=articulo.anio,
                        stockActual=articulo.stockActual,
                        stockMin=articulo.stockMin,
                        stockMax=articulo.stockMax,
                        precioCosto=articulo.precioCosto,
                        precioVenta=articulo.precioVenta,  
                        iva=articulo.iva,
                        proveedor_id=articulo.proveedor_id
                        )
        db.add(new_articulo)
        db.commit()
        db.refresh(new_articulo)
        return new_articulo
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close_all()

# Function to get update the "articulo" is used in "PUT" methods
def updateArticuloDB(id: str, updated_articulo: UpdateArticulo):
    try:
        db = SessionLocal()
        articulo = db.query(ArticuloDB).filter(ArticuloDB.id == id).first()
        print(articulo)
        if articulo:
            articulo.nombre=updated_articulo.nombre
            articulo.tipo=updated_articulo.tipo
            articulo.marca=updated_articulo.marca
            articulo.modelo=updated_articulo.modelo
            articulo.anio=updated_articulo.anio
            articulo.stockActual=updated_articulo.stockActual
            articulo.stockMin=updated_articulo.stockMin
            articulo.stockMax=updated_articulo.stockMax
            articulo.precioCosto=updated_articulo.precioCosto
            articulo.precioVenta=updated_articulo.precioVenta
            articulo.iva=updated_articulo.iva
            articulo.proveedor_id=updated_articulo.proveedor_id

            db.commit()
            db.refresh(articulo)
            return articulo
        return None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Function to remove a "articulo" by their ID, mode logical
def deleteArticuloDB(id: str):
    try:
        db = SessionLocal()
        articulo = db.query(ArticuloDB).filter(ArticuloDB.id == id).first()
        if articulo:
            articulo.activo = False
            db.commit()
            db.refresh(articulo)
        db.close()
        return articulo
    except Exception as e:
        raise e
    finally:
        db.close()
