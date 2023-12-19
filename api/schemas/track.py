from pydantic import BaseModel
from uuid import uuid4

class Track(BaseModel):
    trackid: str = str(uuid4())
    name: str
    composer: str   
    milliseconds: str   
    bytes: str   
    unitprice: str
    album_id : str = str(uuid4())   

class CreateTrackIn(BaseModel):
    name: str
    composer: str   
    milliseconds: str   
    bytes: str   
    unitprice: str
    album_id : str = str(uuid4())      

class CreateTrackOut(BaseModel):
    trackid: str = str(uuid4())
    name: str
    composer: str   
    milliseconds: str   
    bytes: str   
    unitprice: str
    album_id : str = str(uuid4())      

class UpdateTrack(BaseModel):
    name: str
    composer: str   
    milliseconds: str   
    bytes: str   
    unitprice: str
    album_id : str = str(uuid4())   