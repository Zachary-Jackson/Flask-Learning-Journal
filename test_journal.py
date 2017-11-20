import unittest

from playhouse.test_utils import test_database
from peewee import *

import flask_journal
from models import User, Entry

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([User, Entry], safe=True)


USER_DATA = {
    'email': 'test_0@example.com',
    'password': 'password'
}


class UserModelTestCase(unittest.TestCase):
    """This tests the creation and use of a User."""
    @staticmethod
    def create_users(count=2):
        """This creates two users for the following tests."""
        for i in range(count):
            User.create_user(
                email='test_{}@example.com'.format(i),
                password='password'
            )

    def test_create_user(self):
        """This tests to see if the two users in create_method where
        actually created."""
        with test_database(TEST_DB, (User,)):
            self.create_users()
            self.assertEqual(User.select().count(), 2)
            self.assertNotEqual(
                User.select().get().password,
                'password'
            )

    def test_create_duplicate_user(self):
        """This tests to see if an error is given if a user tries to create
        a duplicate user."""
        with test_database(TEST_DB, (User,)):
            self.create_users()
            with self.assertRaises(ValueError):
                User.create_user(
                    email='test_1@example.com',
                    password='password'
                )


class EntryModelTestCase(unittest.TestCase):
    """This tests the creation and use of a Entry."""
    def test_entry_creation(self):
        """This tests if an Entry can be created."""
        with test_database(TEST_DB, (User,)):
            UserModelTestCase.create_users()
            user = User.select().get()
            Entry.create(
            title='Coding',
            entry_date='November the twentieth',
            time_spent='Fifteen minutes',
            learned='Mocking a database with test_database()',
            resources='various online things.'
            )
            entry = Entry.select().get()

            self.assertEqual(
                Entry.select().count(),
                1
            )
            self.assertEqual(entry.title, 'Coding')


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


if __name__ == '__main__':
    unittest.main()
