from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from uuid  import uuid4

# Local imports
from schemas.user import Task
from config import tasks


task = APIRouter()

#Method for Task
@task.get('/{id_user}')
def get_all_task(id_user: str):
    # Send all task of user
    task_dict = {}
    if tasks.__len__() > 0:
        for task in tasks:
            if task['id_user'] == id_user and task['deleted'] == False:
                task_dict[task['id']] = task
        if task_dict.__len__() > 0:
            return task_dict
    # If not found, return 404
    raise HTTPException(status_code=404, detail=f'task: not found')

@task.get('/{id_user}/{id}')
def get_task(id_user: str, id: str):
    # Check if task exists
    if tasks.__len__() > 0:
        # Search for task in database
        task_find = [ task for task in tasks if task['id_user'] == id_user and task['id'] == id and task['deleted'] == False ]
        if task_find.__len__() > 0:
            return task_find[0]
        # If not found, return 404
        raise HTTPException(status_code=404, detail=f'task: {id} not found')
    # If not found, return 404
    raise HTTPException(status_code=404, detail='task: not found')

@task.post('/{id_user}')
def create_task(id_user: str, task: Task):
    task.id = uuid4()
    task.id_user = id_user
    tasks.append(jsonable_encoder(task))
    return task

@task.put('/{id_user}/{id}')
def update_task(id_user: str, id: str, task: Task):
    # Check if task exists
    if task.__len__() > 0:
        # Search for task in database
        task_find = next((i for i, task in enumerate(task) if task['id_user'] == id_user and task["id"] == id and task['deleted'] == False), None)
        if task_find != None:
            task[task_find] = jsonable_encoder(task)
            return task[task_find]
        # If not found, return 404
        raise HTTPException(status_code=404, detail=f'task: {id} not found')
    # If not found, return 404
    raise HTTPException(status_code=404, detail='task: not found')

@task.delete('/{id_user}/{id}')
def delete_task(id_user: str, id: str):
    # Check if task exists
    if task.__len__() > 0:
        # Search for task in database
        task_find = next((i for i, task in enumerate(task) if task['id_user'] == {id_user} and task["id"] == id and task['deleted'] == False), None)
        if task_find != None:
            task[task_find].deleted = not task[task_find].deleted
            return task[task_find]
        # If not found, return 404
        raise HTTPException(status_code=404, detail=f'task: {id} not found')
    # If not found, return 404
    raise HTTPException(status_code=404, detail='task: not found')