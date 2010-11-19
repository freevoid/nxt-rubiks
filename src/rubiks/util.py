import random

from rubiks import FaceType, RotationType
from rubiks.cube import NumpyCube as Cube
from rubiks.face_turn import perform_face_turn

def make_shuffled_cube():
    cube = Cube.solved_cube()

    for i in range(30):
        random_face = random.choice(FaceType.FACES)
        random_direction = random.choice(RotationType.ROTATION_DIRECTION)
        perform_face_turn(cube, (random_face, random_direction))

    return cube

