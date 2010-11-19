import numpy
from cStringIO import StringIO

from rubiks import RotationType, FaceType

class Cube(object):
    def __init__(self, cube_context):
        self._context = cube_context

    def __eq__(self, other):
        return self._context == other._context

    def set_context(self, new_context):
        self._context = new_context

    def get_context(self):
        return self._context

    def pprint(self):
        left = self.get_face(FaceType.LEFT)
        right = self.get_face(FaceType.RIGHT)
        up = self.get_face(FaceType.UP)
        down = self.get_face(FaceType.DOWN)
        front = self.get_face(FaceType.FRONT)
        back = self.get_face(FaceType.BACK)

        f = StringIO()
        f.write("    .---.\n")
        for row in left:
            f.write("    |%s|\n" % ''.join(map(str, row)))
        f.write(".---.---.---.---.\n")
        for row in numpy.concatenate((back, down, front, up), axis=1):
            f.write("|%s%s%s|%s%s%s|%s%s%s|%s%s%s|\n" % tuple(row))
        f.write(".---.---.---.---.\n")
        for row in right:
            f.write("    |%s|\n" % ''.join(map(str, row)))
        f.write("    .---.\n")

        return f.getvalue()

    def __str__(self):
        return self.pprint()


class NumpyCube(Cube):
 
    def __eq__(self, other):
        return all(
                (face == other.get_face(face_name)).all()\
                    for face_name, face in self._context.iteritems()
               )

    def is_valid(self):
        self._context

    def copy(self):
        return NumpyCube(dict((face_name, face.copy())\
                for face_name, face in self._context.iteritems()))

    @classmethod
    def solved_cube(cls):
        context = dict(zip(FaceType.FACES, (cls.make_solid_face(i) for i in range(1,7))))
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
            return face.copy()

    def get_face(self, face_name):
        return self._context[face_name]

    def get_flat_face(self, face_name):
        return self._context[face_name].flat

    def set_face(self, face_name, face):
        self._context[face_name] = face

    def get_faces(self, *faces):
        return map(self.get_face, faces)

    @staticmethod
    def make_solid_face(color):
        return numpy.zeros((3,3), int) + color 

