import unittest

from playhouse.test_utils import test_database
from peewee import *

import flask_journal

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()


# temporary placeholder
# add a create tables here after I update models


USER_DATA = {
    'email': 'test_0@example.com',
    'password': 'password'
}


class UserModelTestCase(unittest.TestCase):
    """This tests the creation and use of a User."""
    @staticmethod
    def create_users(count=2):
        """This creates two users for the following tests."""
        pass

    def test_create_user(self):
        """This tests to see if the two users in create_method where
        actually created."""
        pass

    def test_create_duplicate_user(self):
        """This tests to see if an error is given if a user tries to create
        a duplicate user."""
        pass


class EntryModelTestCase(unittest.TestCase):
    """This tests the creation and use of a Entry."""
    def test_entry_creation(self):
        """This tests if an Entry can be created."""
        pass


class ViewTestCase(unittest.TestCase):
    """This sets up a class to test the web portion of the site."""
    def test_registration(self):
        """This checks if the wording on the site is correct as well as if
        the user gets sent back to the homepage after registering."""
        pass

    def test_good_login(self):
        """This tests a good login."""
        pass

    def test_bad_login(self):
        """This tests a bad login."""
        pass

    def test_logout(self):
        """This tests if the user can logout."""
        pass

    def test_logged_in_menu(self):
        """This tests the wording of the logged_in_menu."""
        pass

    def test_logged_out_menu(self):
        """This tests the wording of the logged_out_menu."""
        pass


class UserViewsTestCase(ViewTestCase):
    """This tests the loggin in and logging out portion of the webpage."""
    def test_entry_create(self):
        """This tests an entry creation from the webpage."""
        pass

    def test_entry_list(self):
        """This tests the list of Entries for validity."""


class EntryViewsTestCase(ViewTestCase):
    """This tests to see if Entries work on the webpage."""
    pass


class EntryEditTestCase(ViewTestCase):
    """This tests the edit Entries portion of the webpage."""
    pass
