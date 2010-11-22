from numpy import array
import rubiks
from rubiks.cube import NumpyCube as Cube
from rubiks.solver import *
from rubiks.util import make_shuffled_cube
from rubiks.solver.fridrich import *
from rubiks.solver.simplest import *
from rubiks.solver import base
from rubiks import *
from rubiks import rotation, cube_operation, face_turn

def try_stage(c, s):
    try:
        return list(s(c))
    except base.StageError as e:
        return e.args[1]

s = SimplestSolver()

sc = Cube.solved_cube()
uc = UnpositionedCross()
pc = PositionCross()

scramle_path = "FUF'DUFRU2L'B2FU2LF'DU'"
c = Cube.from_scramble_path(scramle_path)
rc = make_shuffled_cube()
pcc = cube_operation.perform_united_operations(c.copy(), s.solve(c))

'''Cube(
        {'B': array([[1, 3, 6],
            [5, 5, 1],
            [5, 4, 3]]),
        'D': array([[1, 2, 5],
            [2, 2, 2],
            [6, 2, 3]]),
        'F': array([[3, 4, 1],
            [5, 6, 5],
            [4, 6, 3]]),
        'L': array([[6, 1, 4],
            [4, 3, 5],
            [4, 6, 4]]),
        'R': array([[2, 3, 6],
            [1, 1, 4],
            [2, 3, 5]]),
        'U': array([[5, 6, 2],
            [1, 4, 3],
            [2, 6, 1]])})

'''
