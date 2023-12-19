from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Text, Boolean, Float
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class ArtistDB(Base):
    __tablename__ = "artist"
    artistid = Column(String(250), primary_key=True)
    name = Column(String(50))
    activo = Column(Boolean, default=True)
    albumid = relationship('AlbumDB', backref='artist', lazy=True)

class AlbumDB(Base):
    __tablename__ = "album"
    albumid = Column(String(250), primary_key=True)
    title = Column(String(50))
    activo = Column(Boolean, default=True)    
    artist_id = Column(String(250), ForeignKey('astist.astistid'), nullable=False)
    trackid = relationship('TrackDB', backref='album', lazy=True)

class TrackDB(Base):
    __tablename__ = "track"
    trackid = Column(String(250), primary_key=True)
    name = Column(String(50))
    composer = Column(String(20))
    milliseconds = Column(String(5))
    bytes = Column(String(9))
    unitprice = Column(String(9))
    activo = Column(Boolean, default=True)    
    album_id = Column(String(250), ForeignKey('album.albumid'), nullable=False)

class UsuarioDB(Base):
    __tablename__ = "users"
    id = Column(String(250), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    fullname = Column(String(30))
    email = Column(String(80))
    password = Column(String(50), nullable=False)
    activo = Column(Boolean, default=True)
    isAdmin = Column(Boolean, default=False)