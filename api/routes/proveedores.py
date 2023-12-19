from fastapi import APIRouter
from fastapi import HTTPException
from schemas.proveedor import Proveedor, UpdateProveedor, CreateProveedorIn, CreateProveedorOut
from methods.proveedordb import createProveedorDB, getProveedorDB, getProveedores, updateProveedorDB, deleteProveedorDB
from typing import List

proveedor = APIRouter()

# Method for Proveedores
@proveedor.get('', response_model=List[Proveedor], tags=['Proveedores'])
async def get_all_proveedores():
    # Send all proveedores
    try:
        proveedores = getProveedores()
        if proveedores:
            return proveedores
        # If not found, return 404
        raise HTTPException(status_code=404, detail=f'Proveedores: not found')
    except Exception as e:
        raise HTTPException(status_code=503,detail=f"Error getting proveedores: {e}")

@proveedor.get('/eliminados', response_model=List[Proveedor], tags=['Proveedores'])
async def get_all_proveedores():
    # Send all proveedores
    try:
        proveedores = getProveedores(activo=False)
        if proveedores:
            return proveedores
        # If not found, return 404
        raise HTTPException(status_code=404, detail=f'Proveedores: not found')
    except Exception as e:
        raise HTTPException(status_code=503,detail=f"Error getting proveedores: {e}")
    
@proveedor.get('/{id}', response_model=Proveedor, tags=['Proveedores'])
async def get_proveedor(id: str):
    # Check if proveedores exists
    try:
        proveedor = getProveedorDB(id=id)
        if proveedor:
            return proveedor
        raise HTTPException(status_code=404, detail=f'Proveedor: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error getting proveedor {id}: {e}")

@proveedor.post('', response_model=CreateProveedorOut, tags=['Proveedores'])
async def create_proveedor(proveedor: CreateProveedorIn):
    try:
        new_proveedor = createProveedorDB(proveedor=proveedor)
        return new_proveedor
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: Proveedor creation failed: {e}")

@proveedor.put('/{id}', response_model=UpdateProveedor, tags=['Proveedores'])
async def update_proveedor(id: str, proveedor: UpdateProveedor):
    try:
        updatedProveedor = updateProveedorDB(id=id, updated_proveedor=proveedor)
        if updatedProveedor:
            return updatedProveedor
        raise HTTPException(status_code=404, detail=f'Proveedor: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Update Failed for Proveedor ID: {id}, Error {e}")

@proveedor.delete('/{id}', response_model=Proveedor, tags=['Proveedores'])
async def delete_proveedor(id: str):
    try:
        deleteProveedor = deleteProveedorDB(id=id)
        if deleteProveedor:
            return deleteProveedor
        raise HTTPException(status_code=404, detail=f'Proveedor: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Delete Failed for Proveedor ID: {id}, Error {e}")
