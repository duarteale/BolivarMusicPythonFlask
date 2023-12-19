from fastapi import APIRouter
from fastapi import HTTPException
from schemas.articulo import Articulo, UpdateArticulo, CreateArticuloIn, CreateArticuloOut
from methods.articulodb import createArticuloDB, getArticuloDB, getArticulos, updateArticuloDB, deleteArticuloDB
from typing import List

articulo = APIRouter()

# Method for articulos
@articulo.get('', response_model=List[Articulo], tags=['Articulos'])
async def get_all_articulos():
    # Send all articulos
    try:
        articulos = getArticulos()
        if articulos:
            return articulos
        # If not found, return 404
        raise HTTPException(status_code=404, detail=f'Articulos: not found')
    except Exception as e:
        raise HTTPException(status_code=503,detail=f"Error getting Articulos: {e}")


@articulo.get('/eliminados', response_model=List[Articulo], tags=['Articulos'])
async def get_all_articulos():
    # Send all articulos
    try:
        articulos = getArticulos(activo=False)
        if articulos:
            return articulos
        # If not found, return 404
        raise HTTPException(status_code=404, detail=f'Articulos: not found')
    except Exception as e:
        raise HTTPException(status_code=503,detail=f"Error getting Articulos: {e}")
    
@articulo.get('/{id}', response_model=Articulo, tags=['Articulos'])
async def get_articulo(id: str):
    # Check if articulo exists
    try:
        articulo = getArticuloDB(id=id)
        if articulo:
            return articulo
        raise HTTPException(status_code=404, detail=f'Articulo: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error getting Articulo {id}: {e}")

@articulo.post('', response_model=CreateArticuloOut, tags=['Articulos'])
async def create_articulo(articulo: CreateArticuloIn):
    try:
        new_articulo = createArticuloDB(articulo=articulo)
        return new_articulo
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: Articulo creation failed: {e}")

@articulo.put('/{id}', response_model=UpdateArticulo, tags=['Articulos'])
async def update_articulo(id: str, articulo: UpdateArticulo):
    try:
        updatedArticulo = updateArticuloDB(id=id, updated_articulo=articulo)
        if updatedArticulo:
            return updatedArticulo
        raise HTTPException(status_code=404, detail=f'Articulo: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Update Failed for Articulo ID: {id}, Error {e}")

@articulo.delete('/{id}', response_model=Articulo, tags=['Articulos'])
async def delete_articulo(id: str):
    try:
        deleteArticulo = deleteArticuloDB(id=id)
        if deleteArticulo:
            return deleteArticulo
        raise HTTPException(status_code=404, detail=f'Articulo: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Delete Failed for Articulo ID: {id}, Error {e}")
