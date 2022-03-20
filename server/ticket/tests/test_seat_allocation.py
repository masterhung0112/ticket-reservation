import unittest

from ticket.seat_allocation import mapReservedSeatsToArray, findAvailableSeats

class TestMapReservedSeatsToArray(unittest.TestCase):
    def test_zero_array(self):
        self.assertEqual(mapReservedSeatsToArray(0, []), [])

    def test_one_row_one_seat(self):
        self.assertEqual(mapReservedSeatsToArray(1, ["1A"]), [[[0], [], []]])

    def test_one_row_two_consecutive_seats(self):
        self.assertEqual(mapReservedSeatsToArray(1, ["1A", "1B"]), [[[0, 1], [], []]])

    def test_one_row_two_non_consecutive_seats(self):
        self.assertEqual(mapReservedSeatsToArray(1, ["1A", "1F"]), [[[0], [3], []]])
    
    def test_duplicated_seats(self):
        self.assertEqual(mapReservedSeatsToArray(1, ["1C", "1C"]), [[[], [0], []]])

    def test_unordered_seats(self):
        self.assertEqual(mapReservedSeatsToArray(1, ["1C", "1A", "1B"]), [[[0, 1], [0], []]])

    def test_two_row_two_seats(self):
        self.assertEqual(mapReservedSeatsToArray(2, ["1A", "2A", "2F"]), [[[0], [], []], [[0], [3], []]])

class TestFindAvailableSeats(unittest.TestCase):
    def test_1_seat_0_available(self):
        self.assertEqual(findAvailableSeats(0, 1, [], []), [])

    def test_1_seat_1_available(self):
        self.assertEqual(findAvailableSeats(1, 1, [1], []), [['1A']])

    def test_2_seat_1_available(self):
        with self.assertRaises(Exception):
            findAvailableSeats(1, 1, [1], [])

    def test_4_seat_8_available(self):
        self.assertEqual(findAvailableSeats(1, 4, [2, 4, 2], [[], [], []]), [[], ['1C', '1D', '1E'], []])