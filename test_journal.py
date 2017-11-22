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
        with test_database(TEST_DB, (User, Entry)):
            UserModelTestCase.create_users()
            user = User.select().get()
            Entry.create(
                user=user,
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
            self.assertEqual(entry.user, user)


class ViewTestCase(unittest.TestCase):
    """This sets up a class to test the web portion of the site."""
    def setUp(self):
        flask_journal.app.config['TESTING'] = True
        flask_journal.app.config['WTF_CSRF_ENABLED'] = False
        self.app = flask_journal.app.test_client()


class UserViewsTestCase(ViewTestCase):
    def test_registration(self):
        """This checks if the wording on the site is correct as well as if
        the user gets sent back to the homepage after registering."""
        data = {
            'email': 'test@example.com',
            'password': 'password',
            'password2': 'password'
        }
        with test_database(TEST_DB, (User,)):
            rv = self.app.post(
                '/register',
                data=data)
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, 'http://localhost/')

    def test_good_login(self):
        """This tests a good login."""
        with test_database(TEST_DB, (User,)):
            UserModelTestCase.create_users(1)
            rv = self.app.post('/login', data=USER_DATA)
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, 'http://localhost/')

    def test_bad_login(self):
        """This tests a bad login."""
        with test_database(TEST_DB, (User,)):
            rv = self.app.post('/login', data=USER_DATA)
            self.assertEqual(rv.status_code, 200)

    def test_logout(self):
        """This tests if the user can logout."""
        with test_database(TEST_DB, (User,)):
            # Create and login the user
            UserModelTestCase.create_users(1)
            self.app.post('/login', data=USER_DATA)

            rv = self.app.get('/logout')
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, 'http://localhost/')

    def test_logged_in_menu(self):
        """This tests the wording of the logged_in_menu."""
        with test_database(TEST_DB, (User,)):
            UserModelTestCase.create_users(1)
            self.app.post('/login', data=USER_DATA)
            rv = self.app.get('/')
            self.assertIn("new entry", rv.get_data(as_text=True).lower())
            self.assertIn("logout", rv.get_data(as_text=True).lower())

    def test_logged_out_menu(self):
        """This tests the wording of the logged_out_menu."""
        rv = self.app.get('/')
        self.assertIn("register", rv.get_data(as_text=True).lower())
        self.assertIn("login", rv.get_data(as_text=True).lower())


class EntryViewsTestCase(ViewTestCase):
    """This tests to see if Entries work on the webpage."""
    def test_new_entry_menu(self):
        """This tests to see if the new entry menu is displayed properly."""
        with test_database(TEST_DB, (User,)):
            UserModelTestCase.create_users(1)
            self.app.post('/login', data=USER_DATA)
            rv = self.app.get('/new.html')
            self.assertIn("add entry", rv.get_data(as_text=True).lower())
            self.assertIn("resources", rv.get_data(as_text=True).lower())
            self.assertIn("time spent", rv.get_data(as_text=True).lower())


class DetailsViewsTestCase(ViewTestCase):
    """This tests to see if the details page is displayed properly."""
    def test_details_menu(self):
        with test_database(TEST_DB, (User, Entry)):
            UserModelTestCase.create_users()
            user = User.select().get()
            Entry.create(
                user=user,
                title='Coding',
                entry_date='November the twentieth',
                time_spent='Fifteen minutes',
                learned='Mocking a database with test_database()',
                resources='various online things.'
            )
            entry = Entry.select().get()
            rv = self.app.get('/details.html/{}'.format(entry.id))
            self.assertIn("edit entry", rv.get_data(as_text=True).lower())
            self.assertIn("fifteen", rv.get_data(as_text=True).lower())
            self.assertIn("coding", rv.get_data(as_text=True).lower())


class EditViewsTestCase(ViewTestCase):
    """This tests to see if the edit page is displayed properly."""
    pass


if __name__ == '__main__':
    unittest.main()
