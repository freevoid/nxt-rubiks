from rubiks import FaceType, RotationType
from rubiks.focus import focus_on_face
from rubiks.rotation import rotate_path

def R(cube):
    right = cube.get_face(FaceType.RIGHT)
    cube.set_face(FaceType.RIGHT, cube.rotate_face(right, RotationType.CLOCKWISE))
    back, down, front, up = cube.get_faces(FaceType.BACK, FaceType.DOWN, FaceType.FRONT, FaceType.UP)
    tmp = down[2,:].copy()
    down[2,:] = back[2,:]
    back[2,:] = up[2,:]
    up[2,:] = front[2,:]
    front[2,:] = tmp
    return cube

def Rw(cube):
    right = cube.get_face(FaceType.RIGHT)
    cube.set_face(FaceType.RIGHT, cube.rotate_face(right, RotationType.ANTICLOCKWISE))
    back, down, front, up = cube.get_faces(FaceType.BACK, FaceType.DOWN, FaceType.FRONT, FaceType.UP)
    tmp = down[2,:].copy()
    down[2,:] = front[2,:]
    front[2,:] = up[2,:]
    up[2,:] = back[2,:]
    back[2,:] = tmp
    return cube


def perform_face_turn(cube, (face, rotation_type)):
    if rotation_type == RotationType.DOUBLE_ROTATE:
        cw = RotationType.CLOCKWISE
        return perform_face_turn(
                perform_face_turn(cube, (face, cw)),
                (face, cw))
    
    cube, retpath = focus_on_face(cube, face)
    cube = R(cube) if rotation_type == RotationType.CLOCKWISE else Rw(cube)
    cube, trash = rotate_path(cube, retpath)
    return cube

