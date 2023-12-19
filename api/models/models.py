from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Artist(db.Model):
    artistid = Column(String(250), primary_key=True)
    name = Column(String(50))
    activo = Column(Boolean, default=True)
    albumid = relationship('AlbumDB', backref='artist', lazy=True)

class Album(db.Model):
    albumid = Column(String(250), primary_key=True)
    title = Column(String(50))
    activo = Column(Boolean, default=True)    
    artist_id = Column(String(250), ForeignKey('astist.astistid'), nullable=False)
    trackid = relationship('TrackDB', backref='album', lazy=True)

class Track(db.Model):
    trackid = Column(String(250), primary_key=True)
    name = Column(String(50))
    composer = Column(String(20))
    milliseconds = Column(String(5))
    bytes = Column(String(9))
    unitprice = Column(String(9))
    activo = Column(Boolean, default=True)    
    album_id = Column(String(250), ForeignKey('album.albumid'), nullable=False)

class User(db.Model):
    id = Column(String(250), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    fullname = Column(String(30))
    email = Column(String(80))
    password = Column(String(50), nullable=False)
    activo = Column(Boolean, default=True)
    isAdmin = Column(Boolean, default=False)

    def __str__ (self):
        return f'Id: {self.id}, Nombre de Usuario: {self.username}, E-mail: {self.email}'
