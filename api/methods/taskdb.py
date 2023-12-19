from schemas.usuario import Task, UpdateTask, CreateTask, CompletedTask
from models import TaskDB
from methods.cnx import SessionLocal


# Function to get all task 
def getTasks(id_usuario: str):
    try:
        db = SessionLocal()
        tasks = db.query(TaskDB).filter(TaskDB.id_usuario == id_usuario, TaskDB.deleted == False).all()
        if tasks:
            db.close()
            return tasks
        return None
    except Exception as e:
        raise e
    finally:
        db.close()

# Function to get one task
def getTaskDB(id_usuario: str, id: str):
    try:
        db = SessionLocal()
        task = db.query(TaskDB).filter(TaskDB.id_usuario == id_usuario, TaskDB.id == id).first()
        if task:
            db.close()
            return task
        return None
    except Exception as e:
        raise e
    finally:
        db.close()

# Creation of "Task" is used in the "POST" method
def createTaskDB(id_usuario: str, task: CreateTask):
    try:
        db = SessionLocal()
        new_task = TaskDB(id_usuario=id_usuario,
                          title=task.title,
                          summary=task.summary,
                          )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Function to get update the "task", used in "PUT" methods
def updateTaskDB(id_usuario:str,  id: str, updated_task: UpdateTask):
    try:
        db = SessionLocal()
        task = db.query(TaskDB).filter(TaskDB.id_usuario == id_usuario, TaskDB.id == id).first()

        if task:
            task.title=updated_task.title
            task.summary=updated_task.summary
            task.dateEnd=updated_task.dateEnd
            task.completed=updated_task.completed
            db.refresh(task)
            db.commit()
            db.close()
            return task
        return None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def completTaskDB(id_usuario:str,  id: str, updated_task: CompletedTask):
    try:
        db = SessionLocal()
        task = db.query(TaskDB).filter(TaskDB.id_usuario == id_usuario, TaskDB.id == id).first()

        if task:
            task.dateEnd=updated_task.dateEnd
            task.completed=updated_task.completed
            db.refresh(task)
            db.commit()
            db.close()
            return task
        return None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Function to remove a "task" by their ID
def deleteTaskDB(id_usuario: str, id: str):
    try:
        db = SessionLocal()
        task = db.query(TaskDB).filter(TaskDB.id_usuario == id_usuario, TaskDB.id == id).first()
        if task:
            task.deleted = True
            db.commit()
            db.refresh(task)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
        return task
