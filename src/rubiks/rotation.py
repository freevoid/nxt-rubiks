from rubiks import FaceType, RotationType
    
x_rotation_map = {
    FaceType.FRONT: (RotationType.NO_ROTATION,   FaceType.DOWN),
    FaceType.DOWN:  (RotationType.NO_ROTATION,   FaceType.BACK),
    FaceType.UP:    (RotationType.NO_ROTATION,   FaceType.FRONT),
    FaceType.BACK:  (RotationType.NO_ROTATION,   FaceType.UP),
    FaceType.LEFT:  (RotationType.ANTICLOCKWISE, FaceType.LEFT),
    FaceType.RIGHT: (RotationType.CLOCKWISE,     FaceType.RIGHT)
}

def mapped_rotation(cube, mapping):
    new_context = {}
    for face, (rotation, old_face) in mapping.iteritems():
        new_context[face] = cube.rotate_face(
                cube.get_face(old_face), rotation
                )
    cube.set_context(new_context)

def rotate_x(cube):
    return mapped_rotation(cube, x_rotation_map)

