from datetime import datetime, timedelta
import unittest

from config import TestConfig
from src import create_app, db
from src.models import Book, UserBookEntry

class BookCases(unittest.TestCase):
  def setUp(self):
    self.app = create_app(TestConfig)
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

