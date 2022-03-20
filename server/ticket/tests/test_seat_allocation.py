import unittest

from ticket.seat_allocation import mapReservedSeatsToArray

class TestMapReservedSeatsToArray(unittest.TestCase):
    def test_zero_array(self):
        self.assertEqual(mapReservedSeatsToArray(0, []), [])

    def test_one_row_one_seat(self):
        self.assertEqual(mapReservedSeatsToArray(1, ["1A"]), [[0]])

    def test_one_row_two_consecutive_seats(self):
        self.assertEqual(mapReservedSeatsToArray(1, ["1A", "1B"]), [[0, 1]])

    def test_one_row_two_non_consecutive_seats(self):
        self.assertEqual(mapReservedSeatsToArray(1, ["1A", "1C"]), [[0, 2]])
    
    def test_duplicated_seats(self):
        self.assertEqual(mapReservedSeatsToArray(1, ["1C", "1C"]), [[2]])

    def test_unordered_seats(self):
        self.assertEqual(mapReservedSeatsToArray(1, ["1C", "1A", "1B"]), [[0, 1, 2]])