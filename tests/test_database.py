import unittest
import os
import tempfile
from src.database import TriangleDatabase


class TestTriangleDatabase(unittest.TestCase):

    def setUp(self):
        self.db = TriangleDatabase(db_name=":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_and_get_record(self):
        self.db.add_record(3.0, 4.0, 5.0, "разносторонний", "")
        record = self.db.get_record(3.0, 4.0, 5.0)
        self.assertIsNotNone(record)
        self.assertEqual(record[0], "разносторонний")

    def test_get_nonexistent_record_returns_none(self):
        record = self.db.get_record(1.0, 1.0, 1.0)
        self.assertIsNone(record)

    def test_add_record_replaces_existing(self):
        self.db.add_record(5.0, 5.0, 5.0, "равнобедренный", "")
        self.db.add_record(5.0, 5.0, 5.0, "равносторонний", "")
        record = self.db.get_record(5.0, 5.0, 5.0)
        self.assertEqual(record[0], "равносторонний")

    def test_delete_record(self):
        self.db.add_record(3.0, 4.0, 5.0, "разносторонний", "")
        self.db.delete_record(3.0, 4.0, 5.0)
        record = self.db.get_record(3.0, 4.0, 5.0)
        self.assertIsNone(record)

    def test_error_message_stored(self):
        self.db.add_record(1.0, 2.0, 10.0, "не треугольник", "не треугольник")
        record = self.db.get_record(1.0, 2.0, 10.0)
        self.assertEqual(record[1], "не треугольник")


if __name__ == "__main__":
    unittest.main()