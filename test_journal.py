import unittest


class UserModelTestCase(unittest.Testcase):
    """This tests the creation and use of a User."""
    pass


class EntryModelTestCase(unittest.Testcase):
    """This tests the creation and use of a Entry."""
    pass


class ViewTestCase(unittest.Testcase):
    """This sets up a class to test the web portion of the site."""
    pass


class UserViewsTestCase(ViewTestCase):
    """This tests the loggin in and logging out portion of the webpage."""
    pass


class EntryViewsTestCase(ViewTestCase):
    """This tests to see if Entries work on the webpage."""
    pass


class EntryEditTestCase(ViewTestCase):
    """This tests the edit Entries portion of the webpage."""
    pass
