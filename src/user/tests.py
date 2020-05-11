import unittest

from config import TestConfig
from src import create_app
from src.user.model import db, User

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

  def test_user_creation(self):
    u = User(username='user', email='user@user.com')
    u.set_password('password')
    db.session.add(u)
    db.session.commit()

    self.assertTrue(u.id != None)
    self.assertEqual(u.username, 'user')
    self.assertEqual(u.email, 'user@user.com')
    self.assertEqual(u.is_verified, False)
    self.assertFalse( u.check_password('whatever') )
    self.assertTrue( u.check_password('password') )