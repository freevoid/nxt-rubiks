from rubiks import FaceType, RotationType
from rubiks.rotation import Y, Z, rotate_path, RotationPath

FOCUS_MAP = {
        FaceType.RIGHT: RotationPath([]),
        FaceType.FRONT: RotationPath([(Y, RotationType.ANTICLOCKWISE)]),
        FaceType.BACK: RotationPath([(Y, RotationType.CLOCKWISE)]),
        FaceType.LEFT: RotationPath([(Y, RotationType.CLOCKWISE), (Y, RotationType.CLOCKWISE)]),
        FaceType.UP: RotationPath([(Z, RotationType.CLOCKWISE)]),
        FaceType.DOWN: RotationPath([(Z, RotationType.ANTICLOCKWISE)]),
    }

def focus_on_face(cube, face):
    '''
    Given a cube and face that must be on place of RIGHT face of the
    canonical cube. Performs necessary rotations at returns rotated cube and
    rotation path that will return cube at start position.
    '''
    return rotate_path(cube, FOCUS_MAP[face])

