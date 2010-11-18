import unittest

from rubiks import RotationType, FaceType
from rubiks import cube
from rubiks import rotation

solved_cube_pprinted =\
'''    .---.
    |555|
    |555|
    |555|
.---.---.---.---.
|111|222|333|444|
|111|222|333|444|
|111|222|333|444|
.---.---.---.---.
    |666|
    |666|
    |666|
    .---.
'''

class CubeManipulationsTestCase(unittest.TestCase):
    
    def setUp(self):
        context = dict(zip(FaceType.FACES, (cube.NumpyCube.make_face(i) for i in range(1, 7))))
        self.solved_cube = cube.NumpyCube(context)
        self.face_from_label_list = cube.NumpyCube.face_from_label_list
        self.face = self.face_from_label_list(range(1,10))

    def assertEqualFaces(self, f1, f2):
        self.assertEqual(list(f1.flat), list(f2.flat))

    def test_face_rotations(self):
        face = self.face.copy()
        self.assertEqualFaces(
            self.solved_cube.rotate_face(face, RotationType.CLOCKWISE),
            self.face_from_label_list(
                [7, 4, 1,
                 8, 5, 2,
                 9, 6, 3]))
        
        self.assertEqualFaces(
            self.solved_cube.rotate_face(face, RotationType.ANTICLOCKWISE),
            self.face_from_label_list(
                [3, 6, 9,
                 2, 5, 8,
                 1, 4, 7]))

        self.assertEqualFaces(
            self.solved_cube.rotate_face(face, RotationType.DOUBLE_ROTATE),
            self.face_from_label_list(
                [9, 8, 7,
                 6, 5, 4,
                 3, 2, 1]))

    def test_cube_rotations(self):

        cube = self.solved_cube.copy()

        rotation.rotate(cube, rotation.X, RotationType.CLOCKWISE)
        self.assertNotEqual(cube, self.solved_cube)
        rotation.rotate(cube, rotation.X, RotationType.ANTICLOCKWISE)
        self.assertEqual(cube, self.solved_cube)
        rotation.rotate(cube, rotation.Y, RotationType.CLOCKWISE)
        self.assertNotEqual(cube, self.solved_cube)
        rotation.rotate(cube, rotation.Y, RotationType.ANTICLOCKWISE)
        self.assertEqual(cube, self.solved_cube)
        rotation.rotate(cube, rotation.Z, RotationType.CLOCKWISE)
        self.assertNotEqual(cube, self.solved_cube)
        rotation.rotate(cube, rotation.Z, RotationType.ANTICLOCKWISE)
        self.assertEqual(cube, self.solved_cube)
 
    def test_pprint(self):
        self.assertEqual(self.solved_cube.pprint(), solved_cube_pprinted)


if __name__ == '__main__':
    unittest.main()

