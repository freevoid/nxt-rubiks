import numpy
from rubiks import RotationType, FaceType

class Cube(object):
    def __init__(self, cube_context):
        self._context = cube_context

    def set_context(self, new_context):
        self._context = new_context

class NumpyCube(Cube):
 
    def is_valid(self):
        self._context

    @classmethod
    def solved_cube(cls):
        context = dict(zip(FaceType.FACES, (cls.make_face(i) for i in range(6))))
        return cls(context)

    @staticmethod
    def face_from_label_list(labels):
        return numpy.array(labels).reshape(3,3)
        
    @classmethod
    def rotate_face(cls, face, rotation_type):
        if rotation_type == RotationType.CLOCKWISE:
            ft = face.T
            x = ft.copy()
            x[:, 0] = ft[:, 2]
            x[:, 2] = ft[:, 0]
            return x
        elif rotation_type == RotationType.ANTICLOCKWISE:
            ft = face.T
            x = ft.copy()
            for i in range(3):
                x[::-1, i] = ft[:, i]
            return x
        elif rotation_type == RotationType.DOUBLE_ROTATE:
            return cls.rotate_face(cls.rotate_face(face, RotationType.CLOCKWISE), RotationType.CLOCKWISE)
        else:
            return face

    def get_face(self, face):
        return self._context[face]

    @staticmethod
    def make_face(color):
        return numpy.zeros((3,3), int) + color 

