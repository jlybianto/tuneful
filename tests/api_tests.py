import unittest
import os
import shutil
import json
from urlparse import urlparse
from StringIO import StringIO

import sys; print sys.modules.keys()
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create folder for test uploads
        os.mkdir(upload_path())

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())

    def test_get_uploaded_file(self):
        """ Test of adding a file to an upload folder """
        # Use 'upload_path' function defined in 'utils.py' to get the location of file
        path = upload_path("test.txt")
        with open(path, "w") as f:
            f.write("File contents")
            
        # Send a GET request to '/uploads/<filename>'
        response = self.client.get("/uploads/test.txt")
        
        # Check that the response contains the correct file with correct mimetype
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/plain")
        self.assertEqual(response.data, "File contents")
    
    def test_file_upload(self):
        """ Test to upload simple text file to server """
        # Construct the form data as a dictionary using an instance of 'StringIO' class
        data = {
            "file": (StringIO("File contents"), "test.txt")
        }
        
        # Send this dictionary to endpoint with content type of 'multipart/form-data'
        response = self.client.post("/api/files",
                                   data=data,
                                   content_type="multipart/form-data",
                                   headers=[("Accept", "application/json")]
                                   )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, "application/json")
        
        data = json.loads(response.data)
        self.assertEqual(urlparse(data["path"]).path, "/uploads/test.txt")
        
        path = upload_path("test.txt")
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            contents = f.read()
        self.assertEqual(contents, "File contents")