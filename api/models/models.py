from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Artist(db.Model):
    __tablename__ = 'artist'
    artistid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    albums = relationship('Album', backref='artist', lazy=True, cascade="all, delete-orphan")

class Album(db.Model):
    __tablename__ = 'album'
    albumid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = Column(String(50)) 
    artistid = Column(Integer, ForeignKey('artist.artistid'), nullable=False)
    tracks = relationship('Track', backref='album', lazy=True, cascade="all, delete-orphan")

class Track(db.Model):
    __tablename__ = 'track'
    trackid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    albumid = Column(Integer, ForeignKey('album.albumid'), nullable=False)
    composer = Column(String(20))
    milliseconds = Column(Integer)
    bytes = Column(Integer)
    unitprice = Column(Integer)
    MediaTypeId = db.Column(db.Integer, default=1)

class User(db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    fullname = Column(String(200))
    password = Column(String(120), nullable=False)
    isAdmin = Column(Boolean, default=False)

    def __str__ (self):
        return f'Id: {self.id}, Nombre de Usuario: {self.username}, E-mail: {self.email}'
