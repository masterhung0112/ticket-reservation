
from typing import List, Tuple, Optional
import copy

def mapReservedSeatsToArray(allSeatRowCount: int, reservedSeats: List[str], lotSize: List[int] = [2, 4, 2]) -> List[List[int]]:
    """
    With paramsters (1, ["1A", "1B"]), the method returns [ [ [0, 1], [], [] ] ]
    With paramsters (2, ["1A", "2A", "2B"]), the method returns [
        [[0], [], [] ],
        [[0, 1]], [], [] ]
    ]
    """
    # Generate 3-dimentional array
    allSeats = [[[] for _ in lotSize] for _ in range(allSeatRowCount)]

    # Calculate the maximum number of seats in a row
    maxSeatsInRow = 0
    for lot in lotSize:
        maxSeatsInRow += lot

    for s in reservedSeats:
        # assume that there is only two letters
        if len(s) != 2:
            raise Exception(f"Invalid seat ID {s}")
        
        seatRow = int(s[0]) - 1
        if seatRow >= allSeatRowCount:
            raise Exception(f"Invalid seat row {seatRow}, we have {allSeatRowCount} rows")
        
        seatName = s[1]
        seatNameIndex = ord(seatName) - ord('A')
        if seatRow < 0 or seatNameIndex < 0:
            raise Exception(f"Invalid seat name {s}")

        # Assume the max letter for column is 'H', but we get the value 'I', then raise then exception
        if seatNameIndex >= maxSeatsInRow:
            raise Exception(f"The seat column {seatName} -> {seatNameIndex} exceeds the max column number {maxSeatsInRow}")

        seatLotIndex = 0
        sumLot = 0
        for lot in lotSize:
            if seatNameIndex >= (sumLot + lot):
                seatLotIndex += 1
                sumLot = sumLot + lot
            else:
                break

        # Append the 
        finalSeatNameIndex = seatNameIndex - sumLot
        if finalSeatNameIndex not in allSeats[seatRow][seatLotIndex]:
            allSeats[seatRow][seatLotIndex].append(finalSeatNameIndex)
    
    # Sort the reserved seats in order
    for seatRow in allSeats:
        for seatLot in seatRow:
            seatLot.sort()
    
    return allSeats

class NotEnoughSeatException(Exception):
    pass

# lotSize: (2, 4, 2), targetLotIdx: 2, localColIdx: 0 -> return (2 + 4 + 0)
def lotIdx2ColIdx(targetLotIdx: int, localColIdx: int, lotSize: List[int]) -> int:
    sumLot = 0
    for lotIdx, lot in enumerate(lotSize):
        if lotIdx != targetLotIdx:
            sumLot = sumLot + lot
        else:
            sumLot = sumLot + localColIdx
            break
    return sumLot

def lotLocalIdx2SeatId(rowIdx: int, targetLotIdx: int, localColIdx: int, lotSize: List[int]) -> str:
    return index2SeatId(rowIdx, lotIdx2ColIdx(targetLotIdx, localColIdx, lotSize))
    
def index2SeatId(rowIdx: int, colIdx: int) -> str:
    return f"{rowIdx + 1}{chr(colIdx + ord('A'))}"

def findAvailableSeatsInSlot(targetConsecutiveSeatCount: int, lotSize: List[int], lotEnabled: List[bool], reservedSeats: List[List[int]]):
    found = False
    lotAccumulate = 0

    foundSeated = [[[] for _ in range(len(lotSize))] for _ in range(len(reservedSeats))]

    if len(lotSize) != len(lotEnabled):
        raise Exception("Length of lotEnabled doesn't match length of lotEnabled")
    
    for lotSizeIdx, lot in enumerate(lotSize):
        if lotEnabled[lotSizeIdx] == False:
            lotAccumulate += lot
            continue
    
        # With the lot that have appropriate size
        if lot >= targetConsecutiveSeatCount:
            # For each row of seats
            for seatRowIdx, seatRow in enumerate(reservedSeats):
                lastSeat = -1
                if len(seatRow) != len(lotSize):
                    raise Exception(f"Seat Row slot {len(seatRow)} doesn't match slot size {len(lotSize)}")
                
                # In case the lot size is 4, [0, 1] -> [0, 1, 4]
                allocatedSeatsInRow = seatRow[lotSizeIdx] + [lot]

                # Enumerate each allocated seat, find the free seats between two seats
                for allocatedSeat in allocatedSeatsInRow:
                    # Calculate free seats between two seats
                    free_seats = allocatedSeat - lastSeat - 1

                    # If the free seats is greater than the target seat count, use the first slot
                    if free_seats >= targetConsecutiveSeatCount:
                        for seatLocalIdx in range(lastSeat + 1, lastSeat + 1 + targetConsecutiveSeatCount):
                            foundSeated[seatRowIdx][lotSizeIdx].append(seatLocalIdx)                        
                        found = True
                        break
                    
                    lastSeat = allocatedSeat
                
                if found:
                    break
            
        lotAccumulate += lot
        if found:
            break
    
    return [foundSeated, found]

def findAvailableSeatsFor242(consecutiveSeatCount: int, reservedSeats: List[List[int]]) -> List[List[int]]:
    """
    Find the slots for consecutive seats

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
        [[0, 1], [], [],]
        [[], [0, 1, 2, 3], [0, 1]]
    ]
    """
    
    seat4Slots = 0
    seat2Slots = 0
    seat1Slots = 0

    remaining = consecutiveSeatCount
    if consecutiveSeatCount >= 4:
        seat4Slots = remaining // 4
    remaining -= seat4Slots * 4

    if consecutiveSeatCount >= 2:
        seat2Slots = remaining // 2
    
    remaining -= seat2Slots * 2
    seat1Slots = remaining

    dupReservedSeats = copy.deepcopy(reservedSeats)

    foundSeated = [[[] for _ in [2, 4, 2]] for _ in range(len(reservedSeats))]

    def assignSlot(foundSeatSlots, dupReservedSeats, foundSeated):
        for foundSeatSlotRowIdx, foundSeatSlotRow in enumerate(foundSeatSlots):
            found = False
            for seatSlotIdx, seatSlot in enumerate(foundSeatSlotRow):
                # Found the slot in this row, use the first slot for now
                if len(seatSlot) > 0:
                    dupReservedSeats[foundSeatSlotRowIdx][seatSlotIdx].extend(seatSlot)
                    foundSeated[foundSeatSlotRowIdx][seatSlotIdx].extend(seatSlot)
                    found = True
                    break
            if found == True:
                break
        
    # Handling for 4 seats
    targetConsecutiveSeatCount = 4
    for _ in range (0, seat4Slots):
        foundSeatSlots, found = findAvailableSeatsInSlot(targetConsecutiveSeatCount, [2, 4, 2], [False, True, False], dupReservedSeats)
        if found == False:
            # Split the current slot to the smaller slots
            seat4Slots -= 1
            seat2Slots += 2
        else:
            assignSlot(foundSeatSlots, dupReservedSeats, foundSeated)
    
    targetConsecutiveSeatCount = 2
    for _ in range (0, seat2Slots):
        # Find the 2-seat slot in two sides first
        foundSeatSlots, found = findAvailableSeatsInSlot(targetConsecutiveSeatCount, [2, 4, 2], [True, False, True], dupReservedSeats)
        if found == False:
            # Find the 2-seat slot in 4-seat slot
            foundSeatSlots, found = findAvailableSeatsInSlot(targetConsecutiveSeatCount, [2, 4, 2], [False, True, False], dupReservedSeats)
            if found == False:
                seat2Slots -= 1
                seat1Slots += 2
            else:
                assignSlot(foundSeatSlots, dupReservedSeats, foundSeated)
        else:
            assignSlot(foundSeatSlots, dupReservedSeats, foundSeated)

    targetConsecutiveSeatCount = 1
    for _ in range (0, seat1Slots):
        foundSeatSlots, found = findAvailableSeatsInSlot(targetConsecutiveSeatCount, [2, 4, 2], [True, True, True], dupReservedSeats)
        if found == False:
            raise NotEnoughSeatException("No enough seat")
        else:
            assignSlot(foundSeatSlots, dupReservedSeats, foundSeated)

    print(seat4Slots, seat2Slots, seat1Slots)
    return foundSeated