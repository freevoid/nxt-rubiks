from functools import partial

from rubiks import FaceType, RotationType

X, Y, Z = 'X', 'Y', 'Z'

ROTATION_MAPS = {
    X: {
           RotationType.CLOCKWISE:
                {
                    FaceType.BACK:  (RotationType.NO_ROTATION,   FaceType.UP),
                    FaceType.DOWN:  (RotationType.NO_ROTATION,   FaceType.BACK),
                    FaceType.FRONT: (RotationType.NO_ROTATION,   FaceType.DOWN),
                    FaceType.UP:    (RotationType.NO_ROTATION,   FaceType.FRONT),
                    FaceType.LEFT:  (RotationType.ANTICLOCKWISE, FaceType.LEFT),
                    FaceType.RIGHT: (RotationType.CLOCKWISE,     FaceType.RIGHT)
                },
           RotationType.ANTICLOCKWISE:
                {
                    FaceType.BACK:  (RotationType.NO_ROTATION,   FaceType.DOWN),
                    FaceType.DOWN:  (RotationType.NO_ROTATION,   FaceType.FRONT),
                    FaceType.FRONT: (RotationType.NO_ROTATION,   FaceType.UP),
                    FaceType.UP:    (RotationType.NO_ROTATION,   FaceType.BACK),
                    FaceType.LEFT:  (RotationType.CLOCKWISE,     FaceType.LEFT),
                    FaceType.RIGHT: (RotationType.ANTICLOCKWISE, FaceType.RIGHT)
                }
       },
    Y: {
           RotationType.CLOCKWISE:
                {
                    FaceType.BACK:  (RotationType.CLOCKWISE,   FaceType.RIGHT),
                    FaceType.DOWN:  (RotationType.CLOCKWISE,   FaceType.DOWN),
                    FaceType.FRONT: (RotationType.CLOCKWISE,   FaceType.LEFT),
                    FaceType.UP:    (RotationType.CLOCKWISE,   FaceType.UP),
                    FaceType.LEFT:  (RotationType.CLOCKWISE,   FaceType.BACK),
                    FaceType.RIGHT: (RotationType.CLOCKWISE,   FaceType.FRONT)
                },
           RotationType.ANTICLOCKWISE:
                {
                    FaceType.BACK:  (RotationType.ANTICLOCKWISE, FaceType.LEFT),
                    FaceType.DOWN:  (RotationType.ANTICLOCKWISE, FaceType.DOWN),
                    FaceType.FRONT: (RotationType.ANTICLOCKWISE, FaceType.RIGHT),
                    FaceType.UP:    (RotationType.ANTICLOCKWISE, FaceType.UP),
                    FaceType.LEFT:  (RotationType.ANTICLOCKWISE, FaceType.FRONT),
                    FaceType.RIGHT: (RotationType.ANTICLOCKWISE, FaceType.BACK)
                }
       },
    Z: {
           RotationType.CLOCKWISE:
                {
                    FaceType.BACK:  (RotationType.ANTICLOCKWISE, FaceType.BACK),
                    FaceType.DOWN:  (RotationType.NO_ROTATION,   FaceType.RIGHT),
                    FaceType.FRONT: (RotationType.CLOCKWISE,     FaceType.FRONT),
                    FaceType.UP:    (RotationType.DOUBLE_ROTATE, FaceType.LEFT),
                    FaceType.LEFT:  (RotationType.NO_ROTATION,   FaceType.DOWN),
                    FaceType.RIGHT: (RotationType.DOUBLE_ROTATE, FaceType.UP)
                },
           RotationType.ANTICLOCKWISE:
                {
                    FaceType.BACK:  (RotationType.CLOCKWISE,     FaceType.BACK),
                    FaceType.DOWN:  (RotationType.NO_ROTATION,   FaceType.LEFT),
                    FaceType.FRONT: (RotationType.ANTICLOCKWISE, FaceType.FRONT),
                    FaceType.UP:    (RotationType.DOUBLE_ROTATE, FaceType.RIGHT),
                    FaceType.LEFT:  (RotationType.DOUBLE_ROTATE, FaceType.UP),
                    FaceType.RIGHT: (RotationType.NO_ROTATION,   FaceType.DOWN)
                }
       }
}

def mapped_rotation(cube, mapping):
    new_context = {}
    for face, (rotation, old_face) in mapping.iteritems():
        new_context[face] = cube.rotate_face(
                cube.get_face(old_face).copy(), rotation
                )
    cube.set_context(new_context)

def make_rotation_operations(rotation_maps):
    for axis, rotation_type_map in rotation_maps.iteritems():
        for rotation_type, face_mapping in rotation_type_map.iteritems():
            yield (axis, rotation_type, partial(mapped_rotation, mapping=face_mapping))

def rotate(cube, axis, rotation_direction):
    return OPERATION_MAP[axis][rotation_direction](cube)

OPERATION_MAP = {}
for axis, rotation_type, operation in make_rotation_operations(ROTATION_MAPS):
    axis_dict = OPERATION_MAP.setdefault(axis, {})
    axis_dict[rotation_type] = operation

