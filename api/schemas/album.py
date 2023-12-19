from pydantic import BaseModel
from uuid import uuid4

class Album(BaseModel):
    albumid: str = str(uuid4())
    title: str
    artist_id : str = str(uuid4())

class CreateAlbumIn(BaseModel):
    title: str
    artist_id : str = str(uuid4())

    
class CreateAlbumOut(BaseModel):
    albumid: str = str(uuid4())
    title: str
    artist_id : str = str(uuid4())

class UpdateAlbum(BaseModel):
    title: str
    artist_id : str = str(uuid4())