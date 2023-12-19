from fastapi import APIRouter
from fastapi import HTTPException
from schemas.usuario import *
from methods.usuariodb import *
from typing import List

user = APIRouter()

# Method for Users
@user.get('', response_model=List[User], tags=['Users'])
async def get_all_users():
    # Send all users
    try:
        users = getUsers()
        if users:
            return users
        # If not found, return 404
        raise HTTPException(status_code=404, detail=f'Users: not found')
    except Exception as e:
        raise HTTPException(status_code=503,detail=f"Error getting users: {e}")

@user.get('/eliminados', response_model=List[User], tags=['Users'])
async def get_all_users():
    # Send all users
    try:
        users = getUsers(activo=False)
        if users:
            return users
        # If not found, return 404
        raise HTTPException(status_code=404, detail=f'Users: not found')
    except Exception as e:
        raise HTTPException(status_code=503,detail=f"Error getting users: {e}")
    
@user.get('/{id}', response_model=User, tags=['Users'])
async def get_user(id: str):
    # Check if users exists
    try:
        user = getUsuarioDB(id=id)
        if user:
            return user
        raise HTTPException(status_code=404, detail=f'User: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error getting user {id}: {e}")

@user.post('', response_model=CreateUserOut, tags=['Users'])
async def create_user(user: CreateUser):
    try:
        new_user = createUsuarioDB(user=user)
        return new_user
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: User creation failed: {e}")

@user.put('/{id}', response_model=UpdateUser, tags=['Users'])
async def update_user(id: str, user: UpdateUser):
    try:
        updatedUser = updateUsuarioDB(id=id, updated_user=user)
        if updatedUser:
            return updatedUser
        raise HTTPException(status_code=404, detail=f'User: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Update Failed for User ID: {id}, Error {e}")

@user.delete('/{id}', response_model=User, tags=['Users'])
async def delete_user(id: str):
    try:
        deleteUser = deleteUsuarioDB(id=id)
        if deleteUser:
            return deleteUser
        raise HTTPException(status_code=404, detail=f'User: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Delete Failed for User ID: {id}, Error {e}")


    
@user.post('/login', response_model=User, tags=['Users'])
async def login(user:Login):
    # Check if users exists
    try:
        user = getUserLoginDB(user=user)
        if user:
            return user
        raise HTTPException(status_code=404, detail=f'User: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error getting user {id}: {e}")
    
@user.post('/changepassword', response_model=User, tags=['Users'])
async def changePassword(user:ChangePassword):
    try:
        user = changePasswordDB(user=user)
        if user:
            return user
        raise HTTPException(status_code=404, detail=f'User: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Update Failed for User ID: {id}, Error {e}")