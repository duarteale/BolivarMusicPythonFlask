from fastapi import APIRouter
from fastapi import HTTPException
from schemas.permiso import Permiso, UpdatePermiso, CreatePermisoIn, CreatePermisoOut
from methods.permisodb import createPermisoDB, getPermisoDB, getPermisos, updatePermisoDB, deletePermisoDB
from typing import List

permiso = APIRouter()

@permiso.get('', response_model=List[Permiso], tags=['Permisos'])
async def get_all_permisos():
    try:
        Permiso = getPermisos()
        if Permiso:
            return Permiso
        # If not found, return 404
        raise HTTPException(status_code=404, detail=f'Permisos: not found')
    except Exception as e:
        raise HTTPException(status_code=503,detail=f"Error getting permisos: {e}")

@permiso.get('/eliminados', response_model=List[Permiso], tags=['Permisos'])
async def get_all_permisos():
    try:
        Permiso = getPermisos(activo=False)
        if Permiso:
            return Permiso
        # If not found, return 404
        raise HTTPException(status_code=404, detail=f'Permisos: not found')
    except Exception as e:
        raise HTTPException(status_code=503,detail=f"Error getting permisos: {e}")
    
@permiso.get('/{id}', response_model=Permiso, tags=['Permisos'])
async def get_permiso(id: str):
    # Check if permisoes exists
    try:
        permiso = getPermisoDB(id=id)
        if permiso:
            return permiso
        raise HTTPException(status_code=404, detail=f'Permiso: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error getting permiso {id}: {e}")

@permiso.post('', response_model=CreatePermisoOut, tags=['Permisos'])
async def create_permiso(permiso: CreatePermisoIn):
    try:
        new_permiso = createPermisoDB(permiso=permiso)
        return new_permiso
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: Permiso creation failed: {e}")

@permiso.put('/{id}', response_model=UpdatePermiso, tags=['Permisos'])
async def update_permiso(id: str, permiso: UpdatePermiso):
    try:
        updatedPermiso = updatePermisoDB(id=id, updated_permiso=permiso)
        if updatedPermiso:
            return updatedPermiso
        raise HTTPException(status_code=404, detail=f'Permiso: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Update Failed for Permiso ID: {id}, Error {e}")

@permiso.delete('/{id}', response_model=Permiso, tags=['Permisos'])
async def delete_permiso(id: str):
    try:
        deletePermiso = deletePermisoDB(id=id)
        if deletePermiso:
            return deletePermiso
        raise HTTPException(status_code=404, detail=f'Permiso: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Delete Failed for Permiso ID: {id}, Error {e}")