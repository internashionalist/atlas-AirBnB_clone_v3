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
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
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


@unittest.skipIf(models.storage_t == "db", "not testing file storage")
class TestFileStorage(unittest.TestCase):
    """
    tests the FileStorage class
    """
    def test_all_returns_dict(self):
        """
        tests that 'all' returns a dictionary
        """
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    def test_new(self):
        """
        tests that 'new' adds an object to the storage dictionary
        """
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    def test_save(self):
        """
        tests that 'save' properly saves objects to file.json
        """
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    def test_reload(self):
        """
        tests that 'reload' properly reloads objects from file.json
        """
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        storage.reload()
        for key, value in new_dict.items():
            self.assertTrue(value == storage._FileStorage__objects[key])

    def test_delete(self):
        """
        tests that 'delete' properly deletes objects from __objects
        """
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.delete(new_dict[instance_key])
        self.assertNotIn(instance_key, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    def test_get(self):
        """
        tests that 'get' retrieves one object
        """
        storage = FileStorage()
        instance = State(name="Oklahoma")
        instance.save()
        got_instance = storage.get(State, instance.id)
        self.assertEqual(instance, got_instance)
        storage.delete(instance)

    def test_count(self):
        """
        tests that 'count' counts the number of objects in storage
        """
        storage = FileStorage()
        initial_count = storage.count()

        state_instance = State(name="Oklahoma")
        state_instance.save()
        self.assertEqual(storage.count(State), initial_count + 1)

        self.assertEqual(storage.count(), initial_count + 1)

        storage.delete(state_instance)
        self.assertEqual(storage.count(State), initial_count)
