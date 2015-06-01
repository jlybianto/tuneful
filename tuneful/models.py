import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from database import Base, engine

class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True)
    file = relationship("File", uselist=False, backref="song")
    
    def asDictionary(self):
        return {
            "id": 1,
            "file": {
                "id": 7,
                "name": "Shady_Grove.mp3"
            }
        }

class File(Base):
    ___tablename__ = "files"
    id = Column(Integer, primary_key=True)
    filename = Column(String(1024))
    song_id = Column(Integer, ForeignKey("songs.id"))
    
    def asDictionary(self):
        return {
            "id": 7,
            "name": "Shady_Grove.mp3"
        }