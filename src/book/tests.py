import unittest

from config import TestConfig
from src import create_app
from src.book.model import db, Book

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

  def test_book_creation(self):
    b = Book(title='book one', author='some author')
    db.session.add(b)
    db.session.commit()

    self.assertEqual(b.title, 'book one')
    self.assertEqual(b.author, 'some author')
    self.assertTrue(b.id != None)