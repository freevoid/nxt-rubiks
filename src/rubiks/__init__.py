class RotationType:
    NO_ROTATION = 'no-rotation'
    DOUBLE_ROTATE = 'double-clockwise'
    CLOCKWISE = 'clockwise'
    ANTICLOCKWISE = 'anti-clockwise'
    ROTATION_DIRECTION = (CLOCKWISE, ANTICLOCKWISE)

class FaceType:
    FRONT = 'F'
    BACK = 'B'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'

    FACES = (BACK, DOWN, FRONT, UP, LEFT, RIGHT)
    ENUMERATED_FACES = [(i+1, face) for (i, face) in enumerate(FACES)]

CUBE_ROTATION = 'cube rotation'
QUARTER_FACE_ROTATION = 'quarter face rotation'

OPERATION_TYPES = (
    CUBE_ROTATION,
    QUARTER_FACE_ROTATION,
    )

