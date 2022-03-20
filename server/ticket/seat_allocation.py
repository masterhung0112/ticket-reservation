
from typing import List, Set, Dict, Tuple, Optional

"""
Find the slots for 2 consecutive seats

Example of row
1 A B   C D E F  G H
2 A B   C D E F  G H

Each row has three arrays
1 [[], [], []]
2 [[], [], []]

In case we have reserved seats at 1A, 2C and 2D
1 [[0], [], []]
2 [[], [0, 1], []]

With the array length of (2, 4, 2),
At element(0, 0), the remaining length of array is (2 - 1), not appropriate
At element(0, 1), the remaining length of array is (4 - 0), appropriate
At element(0, 2), the remaining length of array is (2 - 0), appropriate

At element(1, 0), the remaining length of array is (2 - 0), appropriate
At element(1, 1), analyzing the free seats for [0, 1]
    For element 0, [0 - (-1) - 1] = 0
    For element 1, [1 - 0 - 1] = 0
    For element 2, [4 - 1 - 1] = 2, appropriate 2E and 2F

At element(1, 2), the remaining length of array is (2 - 0), appropriate

Return value:
[
    [[1C, 1D], [1D, 1E], [1E, 1F], [1G, 1H],]
    [[2A, 2B], [2E, 2F], [3G, 3H]]
]
"""

def mapReservedSeatsToArray(allSeatRowCount: int, reservedSeats: List[str], maxSeatColCount = 8) -> List[List[int]]:
    """
    With paramsters (1, ["1A", "1B"]), the method eturns [[0, 1]]
    With paramsters (2, ["1A", "2A", "2B"]), the method returns [[0], [0, 1]]
    """
    # Generate 2-dimentional array
    allSeats = [[] for _ in range(allSeatRowCount)]

    for s in reservedSeats:
        # assume that there is only two letters
        if len(s) != 2:
            raise Exception(f"Invalid seat ID {s}")
        
        seatRow = int(s[0]) - 1
        if seatRow >= allSeatRowCount:
            raise Exception(f"Invalid seat row {seatRow}, we have {allSeatRowCount} rows")
        
        seatName = s[1]
        seatNameIndex = ord(seatName) - ord('A')

        # Assume the max letter for column is 'H', but we get the value 'I', then raise then exception
        if seatNameIndex >= maxSeatColCount:
            raise Exception(f"The seat column {seatName} -> {seatNameIndex} exceeds the max column number {maxSeatColCount}")

        if seatNameIndex not in allSeats[seatRow]:
            allSeats[seatRow].append(seatNameIndex)
    
    # Sort the reserved seats in order
    for seatRow in allSeats:
        seatRow.sort()
    
    return allSeats

def findAvailableSeats(allSeatRowCount: int, reservedSeats: List[List[int]]) -> List[List[str]]:
    return []