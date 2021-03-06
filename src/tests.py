import unittest

from rubiks import RotationType, FaceType
from rubiks import cube
from rubiks import rotation
from rubiks import face_turn
from rubiks import cube_operation
from rubiks.solver import common_patterns

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

class CubeTestCaseBase(unittest.TestCase):

    def setUp(self):
        self.solved_cube = cube.NumpyCube.solved_cube()
        self.face_from_label_list = cube.NumpyCube.face_from_label_list
        self.face = self.face_from_label_list(range(1,10))

    def assertEqualFaces(self, f1, f2):
        self.assertEqual(list(f1.flat), list(f2.flat))


class CubeManipulationsTestCase(CubeTestCaseBase):

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

        rotation.rotate(cube, (rotation.X, RotationType.CLOCKWISE))
        self.assertNotEqual(cube, self.solved_cube)
        rotation.rotate(cube, (rotation.X, RotationType.ANTICLOCKWISE))
        self.assertEqual(cube, self.solved_cube)
        rotation.rotate(cube, (rotation.Y, RotationType.CLOCKWISE))
        self.assertNotEqual(cube, self.solved_cube)
        rotation.rotate(cube, (rotation.Y, RotationType.ANTICLOCKWISE))
        self.assertEqual(cube, self.solved_cube)
        rotation.rotate(cube, (rotation.Z, RotationType.CLOCKWISE))
        self.assertNotEqual(cube, self.solved_cube)
        rotation.rotate(cube, (rotation.Z, RotationType.ANTICLOCKWISE))
        self.assertEqual(cube, self.solved_cube)
 
    def test_pprint(self):
        self.assertEqual(self.solved_cube.pprint(), solved_cube_pprinted)

    def test_comlex_operations(self):
        cube = self.solved_cube.copy()
        # make some crazy moves
        self.assertEqual(str(cube_operation.perform_coded_operations(cube, "FUD2xB2y2R'z'L'F2D'")),
'''    .---.
    |254|
    |236|
    |533|
.---.---.---.---.
|664|125|245|341|
|121|266|145|355|
|666|352|345|211|
.---.---.---.---.
    |426|
    |313|
    |441|
    .---.
''')
        # perform opposite moves
        cube_operation.perform_coded_operations(cube, "DF2LzRy2B2x'D2U'F'")
        # assert that cube is back to start position
        self.assertEqual(cube, self.solved_cube)

    def test_all_positions_iteration(self):
        cube = self.solved_cube.copy()
        # check that all positions in iteration are unique
        iterated = []
        for c, p, bp in rotation.iterate_all_positions(cube):
            self.assertTrue(c not in iterated)
            iterated.append(c.copy())

        # check that there are exactly 24 unique positions
        self.assertEqual(len(iterated), 24)
        # check that iteration didn't affected argument after all
        # self.assertEqual(cube, self.solved_cube)


class CubePatternsTestCase(CubeTestCaseBase):

    def test_basic_patterns(self):
        self.assertTrue(self.solved_cube, common_patterns.cross_pattern)
        self.assertTrue(self.solved_cube, common_patterns.f2l_pattern)
        self.assertTrue(self.solved_cube, common_patterns.done_pattern)

        cube = self.solved_cube.copy()

        cube = face_turn.perform_face_turn(cube, (FaceType.UP, RotationType.CLOCKWISE))
        self.assertTrue(common_patterns.cross_pattern.match_pattern(cube))
        self.assertTrue(common_patterns.f2l_pattern.match_pattern(cube))
        self.assertFalse(common_patterns.done_pattern.match_pattern(cube))

        cube = face_turn.perform_face_turn(cube, (FaceType.RIGHT, RotationType.CLOCKWISE))
        self.assertFalse(common_patterns.cross_pattern.match_pattern(cube))
        self.assertFalse(common_patterns.f2l_pattern.match_pattern(cube))
        self.assertFalse(common_patterns.done_pattern.match_pattern(cube))

if __name__ == '__main__':
    unittest.main()

