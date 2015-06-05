import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

import models
import decorators
from tuneful import app
from database import session
from utils import upload_path

@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/json")
def songs_get():
    """ Get a list of songs """
    # Get the songs from the database
    songs = session.query(models.Song).all()
    
    # Convert the songs to JSON and return a response
    data = json.dumps([song.asDictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/songs", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
def song_post():
    """ Add a song """
    # To access the data passed into the endpoint
    data = request.json
    file = session.query(models.File).get(data["file"]["id"])
    
    # Check whether the song file exists
    # If no, return a 404 with a helpful message
    if not file:
        message = "Could not find song file with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
    
    # Add the song file to the database
    song = models.Song(file=file)
    session.add(song)
    session.commit()
    
    # Return a 201 Created, containing the song file as JSON
    data = json.dumps(song.asDictionary())
    return Response(data, 201, mimetype="application/json")

@app.route("/api/songs/<int:id>", methods=["PUT"])
@decorators.accept("application/json")
@decorators.require("application/json")
def song_edit(id):
    """ Edit a song """
    # To access the data passed into the endpoint
    data = request.json
    
    # Get the song file from the database
    file = session.query(models.File).get(id)
    
    # Check whether the song file exists
    # If no, return a 404 with a helpful message
    if not song:
        message = "Could not find song file with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # If yes, gives ability to edit the song
    song.name = data["name"]
    session.add(song)
    session.commit()
    return Response(data, 200, mimetype="application/json")

@app.route("/api/songs/<int:id>", methods=["DELETE"])
@decorators.accept("application/json")
def song_delete(id):
    """ Delete a song """    
    # Get the song file from the database
    file = session.query(models.File).get(id)
    
    # Check whether the song file exists
    # If no, return a 404 with a helpful message
    if not file:
        message = "Could not find song file with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
    
    # If yes, delete the song from database with confirmation message
    session.delete(song)
    session.commit()
    message = "Deleted song with id {} from database".format(id)
    data = json.dumps({"message": message})
    return Response(data, 200, mimetype="application/json")