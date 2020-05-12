import unittest

from config import TestConfig
from src import create_app, db
from src.models import User

class UserCases(unittest.TestCase):
  def setUp(self):
    self.app = create_app(TestConfig)
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_check_password(self):
    u = User(username='user', email='user@user.com')
    u.set_password('password')
    db.session.add(u)
    db.session.commit()

    self.assertFalse( u.check_password('whatever') )
    self.assertTrue( u.check_password('password') )

  def test_entry_creation(self):
    u = User(username='u', email='u@u.com')
    db.session.add(u)
    db.session.commit()

    title = 'book one'
    author = 'some author'

    res1 = u.add_entry_to_collection(title=title, author=author)
    res2 = u.add_entry_to_collection(title=title, author=author)
    res3 = u.add_entry_to_collection(title='other title', author='other author')
    db.session.commit()

    # res1 = res2 b/c trying to insert same book shouldn't duplicate anything
    # collection() should be equal to [ first_entry, second_entry ]
    self.assertEqual(res1, res2)
    self.assertEqual( u.collection().all(), [res1, res3] )