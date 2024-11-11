#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """
    tests the DBStorage class and its methods
    """
    def setUp(self):
        """
        sets up before each test
        """
        storage = DBStorage()
        storage.reload()

    def tearDown(self):
        """
        deletes the storage instance and the file.json after each test
        """
        self.storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """
        tests that 'all' returns a dictionary
        """
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """
        tests that 'all' returns all rows when no class is passed
        """
        storage = DBStorage()
        obj = storage.all()
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage.all())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """
        tests that 'new' adds an object to the database
        """
        initial_objs = self.storage.all(State)
        state = State(name="Oklahoma")
        self.storage.new(state)
        self.storage.save()
        self.assertNotEqual(initial_objs, self.storage.all(State))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """
        tests that 'save' saves an object to the database
        """
        initital_objs = self.storage.all(State)
        state = State(name="Oklahoma")
        self.storage.new(state)
        self.storage.save()
        self.assertNotEqual(initital_objs, self.storage.all(State))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """
        tests that 'get' retrieves an object from storage
        """
        state = State(name="Oklahoma")
        self.storage.new(state)
        self.storage.save()
        obj = self.storage.get(State, state.id)
        self.assertEqual(obj, state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """
        tests that 'count' returns the number of objects in storage
        """
        initial_count = self.storage.count(State)
        state = State(name="Oklahoma")
        self.storage.new(state)
        self.storage.save()
        self.assertEqual(self.storage.count(State), initial_count + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete(self):
        """
        tests that 'delete' deletes an object from storage
        """
        state = State(name="Oklahoma")
        self.storage.new(state)
        self.storage.save()
        self.storage.delete(state)
        self.assertIsNone(self.storage.get(State, state.id))
