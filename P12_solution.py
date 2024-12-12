#!/usr/local/bin/python
from P12_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
#from Pxx_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT1 = DEMO_INPUT1.strip()
    INPUT2 = DEMO_INPUT2.strip()
    DEBUG = True
else:
    INPUT1 = PRODUCTION_INPUT.strip()
    INPUT2 = INPUT1
    DEBUG = False


def debug(s, new_line_before=False, new_line_after=False):
    if DEBUG:
        if new_line_before:
            print()
        print(s)
        if new_line_after:
            print()


INPUT = INPUT1

data = INPUT.splitlines()
ROWCOUNT = len(data)
COLCOUNT = len(data[0])

cell_to_region = dict()     # location -> region
regionid_to_cells = dict()  # regionid -> set of locations
new_regionid = 0

# Determine regions
for rownum in range(ROWCOUNT):
    for colnum in range(COLCOUNT):
        if (rownum, colnum) in cell_to_region:
            # We already know the region of this location
            continue
        region_name = data[rownum][colnum]
        region_cells = set()
        region_cells.add((rownum, colnum))
        boundary_cells = set()
        boundary_cells.add((rownum, colnum))
        while True:
            new_cells = set()
            for rownum2, colnum2 in boundary_cells:
                if rownum2 > 0 and data[rownum2-1][colnum2] == region_name:
                    new_cells.add((rownum2-1, colnum2))
                if colnum2 > 0 and data[rownum2][colnum2-1] == region_name:
                    new_cells.add((rownum2, colnum2-1))
                if rownum2 < ROWCOUNT-1 and data[rownum2+1][colnum2] == region_name:
                    new_cells.add((rownum2+1, colnum2))
                if colnum2 < COLCOUNT-1 and data[rownum2][colnum2+1] == region_name:
                    new_cells.add((rownum2, colnum2+1))
            new_cells.difference_update(region_cells)
            if len(new_cells) == 0:
                break
            region_cells.update(new_cells)
            boundary_cells = new_cells
        regionid_to_cells[new_regionid] = region_cells
        for rownum2, colnum2 in region_cells:
            cell_to_region[(rownum2, colnum2)] = new_regionid
        new_regionid += 1


regionid_to_boundary = dict() # regionid -> set of boundary items

for regionid, region_cells in regionid_to_cells.items():
    region_size = len(region_cells)
    # Set of boundary items { (rownum, colnum, is_horizontal), ... }
    #   If is_horizontal:     boundary is UNDER (rownum, colnum)
    #   If not is_horizontal: boundary is to the RIGHT of (rownum, colnum)
    boundary = set()
    for rownum, colnum in region_cells:
        if (rownum-1, colnum) not in region_cells:
            boundary.add((rownum-1, colnum, True))
        if (rownum+1, colnum) not in region_cells:
            boundary.add((rownum, colnum, True))
        if (rownum, colnum-1) not in region_cells:
            boundary.add((rownum, colnum-1, False))
        if (rownum, colnum+1) not in region_cells:
            boundary.add((rownum, colnum, False))
    regionid_to_boundary[regionid] = boundary


# Part 1

total_price = 0
for regionid, region_cells in regionid_to_cells.items():
    region_size = len(region_cells)
    boundary_length = len(regionid_to_boundary[regionid])
    price = region_size * boundary_length
    total_price += price
print(f'Part 1 - Total price {total_price}')



# Part 2

DIRECTION_RIGHT = 'right'
DIRECTION_LEFT = 'left'
DIRECTION_UP = 'up'
DIRECTION_DOWN = 'down'

def count_number_of_corners(boundary):
    debug(boundary, True, True)
    num_corners = 0
    while len(boundary) > 0:
        # Pick arbitrary remaining boundary element and follow its border, and count number of corners encountered
        start_b = next(iter(boundary))  # pick but do not remove an arbitrary element
        if start_b[2]:
            last_direction = DIRECTION_RIGHT
        else:
            last_direction = DIRECTION_DOWN
        debug(f'Staring boundary at {start_b} direction {last_direction}')
        b = start_b
        back_to_start = False
        while not back_to_start:
            rownum, colnum, is_horizontal = b
            debug(f'  Expanding boundary at {b} - last_direction is {last_direction} - num_corners is {num_corners} so far')
            try_boundaries = list()
            # Note first try 2 corners, only after that try going straight. Otherwise errors such as self-crossing
            if last_direction == DIRECTION_RIGHT:
                try_boundaries.append(((rownum, colnum, False), DIRECTION_UP))
                try_boundaries.append(((rownum+1, colnum, False), DIRECTION_DOWN))
                try_boundaries.append(((rownum, colnum+1, True), DIRECTION_RIGHT))
            elif last_direction == DIRECTION_LEFT:
                try_boundaries.append(((rownum, colnum-1, False), DIRECTION_UP))
                try_boundaries.append(((rownum+1, colnum-1, False), DIRECTION_DOWN))
                try_boundaries.append(((rownum, colnum-1, True), DIRECTION_LEFT))
            elif last_direction == DIRECTION_DOWN:
                try_boundaries.append(((rownum, colnum, True), DIRECTION_LEFT))
                try_boundaries.append(((rownum, colnum+1, True), DIRECTION_RIGHT))
                try_boundaries.append(((rownum+1, colnum, False), DIRECTION_DOWN))
            elif last_direction == DIRECTION_UP:
                try_boundaries.append(((rownum-1, colnum, True), DIRECTION_LEFT))
                try_boundaries.append(((rownum-1, colnum+1, True), DIRECTION_RIGHT))
                try_boundaries.append(((rownum-1, colnum, False), DIRECTION_UP))
            for b2, new_direction in try_boundaries:
                if b2 in boundary:
                    boundary.remove(b2)
                    if b2[2] != is_horizontal:
                        num_corners += 1
                    if b2 == start_b:
                        back_to_start = True
                        debug('  Back to start')
                    b = b2
                    last_direction = new_direction
                    break
    return num_corners

total_price = 0
for regionid, region_cells in regionid_to_cells.items():
    region_size = len(region_cells)
    boundary_length = count_number_of_corners(regionid_to_boundary[regionid])
    debug(f'Region {regionid} - size {region_size} - len {boundary_length}')
    price = region_size * boundary_length
    total_price += price
print(f'Part 2 - Total price {total_price}')



