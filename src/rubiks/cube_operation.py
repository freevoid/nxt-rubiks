from rubiks import FaceType, RotationType

def R(cube):
    front = cube.get_face(FaceType.FRONT)
    cube.set_face(FaceType.FRONT, cube.rotate_face(front, RotationType.CLOCKWISE))
    back, down, front, up = cube.get_faces(FaceType.BACK, FaceType.DOWN, FaceType.FRONT, FaceType.UP)
    tmp = down[2,:].copy()
    down[2,:] = back[2,:]
    back[2,:] = up[2,:]
    up[2,:] = front[2,:]
    front[2,:] = tmp

