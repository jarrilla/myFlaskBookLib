from datetime import datetime, timedelta
import unittest

from config import TestConfig
from src import create_app, db
from src.book.models import Book, UserBookEntry

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

# Make some books and some UserBookEntries, check that book entries correctly point to books
  def test_new_book_entry_refs(self):
    b1 = Book(title='book one', author='some author')
    b2 = Book(title='book two', author='some author')
    b3 = Book(title='book three', author='some author')
    db.session.add(b1)
    db.session.add(b2)
    db.session.add(b3)
    db.session.commit()

    today = datetime.now().date()

    e1 = UserBookEntry( book_id=b1.id)
    e2 = UserBookEntry( book_id=b1.id)
    e3 = UserBookEntry( book_id=b2.id)
    e4 = UserBookEntry( book_id=b3.id)
    db.session.add(e1)
    db.session.add(e2)
    db.session.add(e3)
    db.session.add(e4)
    db.session.commit()

    self.assertEqual(e1.book, b1)
    self.assertEqual(e2.book, b1)
    self.assertEqual(e3.book, b2)
    self.assertEqual(e4.book, b3)