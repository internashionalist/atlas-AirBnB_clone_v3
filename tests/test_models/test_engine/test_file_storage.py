#!/usr/bin/python3
"""
This module contains the tests for the FileStorage class.
"""

from datetime import datetime
import inspect
import json
import models
import pep8
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity,
           "BaseModel": BaseModel,
           "City": City,
           "Place": Place,
           "Review": Review,
           "State": State,
           "User": User
           }


class TestFileStorageDocs(unittest.TestCase):
    """
    checks the documentation and style of FileStorage class
    """
    @classmethod
    def setUpClass(cls):
        """
        sets up the doc tests
        """
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """
        tests conformity to PEP8
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """
        tests test conformity to PEP8"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
                                    test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """
        tests for the presence of a docstring in the module
        """
        self.assertIsNot(FileStorage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """
        tests for the presence of a docstring in the class
        """
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """
        tests for the presence of docstrings in the methods
        """
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """
    tests the FileStorage class
    """

    def setUp(self):
        """
        clears storage before each test
        """
        self.storage = FileStorage()
        self.storage._FileStorage__objects.clear()

    def tearDown(self):
        """
        resets storage after each test
        """
        self.storage._FileStorage__objects.clear()

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_all_returns_dict(self):
        """
        tests that 'all' returns a dictionary
        """
        new_dict = self.storage.all()
        self.assertIsInstance(new_dict, dict)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_new(self):
        """
        tests that 'new' adds an object to the storage dictionary
        """
        for key, value in classes.items():
            instance = value()
            instance.save()
            instance_key = f"{instance.__class__.__name__}.{instance.id}"
            self.assertIn(instance_key, self.storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_save(self):
        """
        tests that 'save' properly saves objects to file.json
        """
        st_instance = State(name="Oklahoma")
        self.storage.new(st_instance)
        self.storage.save()
        with open("file.json", "r") as file:
            file_stuff = json.load(file)
        instance_key = f"{st_instance.__class__.__name__}.{st_instance.id}"
        self.assertIn(instance_key, file_stuff)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_reload(self):
        """
        tests that 'reload' properly reloads objects from file.json
        """
        c_instance = City(name="Tulsa")
        self.storage.new(c_instance)
        self.storage.save()
        self.storage._FileStorage__objects.clear()
        self.storage.reload()
        instance_key = f"{c_instance.__class__.__name__}.{c_instance.id}"
        self.assertIn(instance_key, self.storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_delete(self):
        """
        tests that 'delete' properly deletes objects from __objects
        """
        u_instance = User(email="suuu@wutang.com", password="forever")
        self.storage.new(u_instance)
        instance_key = f"{u_instance.__class__.__name__}.{u_instance.id}"
        self.storage.delete(u_instance)
        self.assertNotIn(instance_key, self.storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_get(self):
        """
        tests that 'get' retrieves one object
        """
        instance = State(name="Oklahoma")
        self.storage.new(instance)
        self.storage.save()
        self.storage.reload()
        got_instance = self.storage.get(State, instance.id)
        self.assertEqual(instance.id, got_instance.id)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_count(self):
        """
        tests that 'count' counts the number of objects in storage
        """
        initial_count = self.storage.count()
        state_instance = State(name="Oklahoma")
        state_instance.save()
        self.assertEqual(self.storage.count(), initial_count + 1)
        self.assertEqual(self.storage.count(State), 1)
