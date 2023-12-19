from pydantic import BaseModel
from uuid import uuid4

class Artist(BaseModel):
    artistid: str = str(uuid4())
    name: str    

class CreateArtistIn(BaseModel):
    name: str
    
class CreateArtistOut(BaseModel):
    artistid: str = str(uuid4())
    name: str

class UpdateArtist(BaseModel):
    name: str