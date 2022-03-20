import unittest

from ticket.seat_allocation import mapReservedSeatsToArray, findAvailableSeatsFor242, index2SeatId, findAvailableSeatsInSlot, lotIdx2ColIdx

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

class TestFindAvailableSeatsInSlot(unittest.TestCase):
    def test_1_seat(self):
        self.assertEqual(findAvailableSeatsInSlot(4, [2, 4, 2], [False, True, False], [[[], [], []]]), [[[[], [0, 1, 2, 3], []]], True])

        self.assertEqual(findAvailableSeatsInSlot(1, [2, 2, 2], [True, True, True], [[[0], [0, 1], []]]), [[[[1], [], []]], True])

        # Not found if the 4-seat slot is disabled
        self.assertEqual(findAvailableSeatsInSlot(4, [2, 4, 2], [True, False, True], [[[], [], []]]), [[[[], [], []]], False])

class TestFindAvailableSeats(unittest.TestCase):
    def test_1_seat_0_row(self):
        with self.assertRaises(Exception):
            findAvailableSeatsFor242(1, []), []

    def test_1_seat_1_row(self):
        self.assertEqual(findAvailableSeatsFor242(1, [[[], [], []]]), [[[0], [], []]])

    def test_2_seat_1_available(self):
        with self.assertRaises(Exception):
            findAvailableSeatsFor242(1, [])

    def test_4_seats(self):
        self.assertEqual(findAvailableSeatsFor242(4, [[[], [], []]]), [[[], [0, 1, 2, 3], []]])
        
        # No free 4-seat slot, use 2-seat slot
        self.assertEqual(findAvailableSeatsFor242(4, [[[0], [0], [0]]]), [[[1], [1, 2, 3], []]])

        # Foudn the slot at the second row
        self.assertEqual(findAvailableSeatsFor242(
            4,
            [
                [[0], [0], [0]], 
                [[], [], []]
            ]
        ), [[[], [], []], [[], [0, 1, 2, 3], []]])
    
    def test_2_seats(self):
        self.assertEqual(findAvailableSeatsFor242(2, [[[], [], [1]]]), [[[0, 1], [], []]])
        self.assertEqual(findAvailableSeatsFor242(2, [[[1], [], [1]]]), [[[], [0, 1], []]])

class TestIndex2SeatId(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(index2SeatId(0, 0), "1A")
        self.assertEqual(index2SeatId(0, 1), "1B")
        self.assertEqual(index2SeatId(7, 7), "8H")

class TestLotIdx2ColIdx(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(lotIdx2ColIdx(2, 0, [2, 4, 4]), 6)
        self.assertEqual(lotIdx2ColIdx(1, 3, [2, 4, 4]), 5)

