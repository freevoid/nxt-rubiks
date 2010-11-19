from itertools import izip

from rubiks import FaceType, RotationType
from rubiks import rotation
from rubiks import cube_operation
from rubiks.cube import NumpyCube as Cube

make_face = Cube.face_from_label_list

__all__ = ('CubePattern', 'ExactCubePattern', 'CubePatternWithAction',
        'ExactCubePatternWithAction', 'SolveStage', 'SolvingProcess')

class CubePattern(object):

    def __init__(self, pattern):
        self._pattern = pattern
        super(CubePattern, self).__init__()

    def check_at_all_positions(self, cube):
        for cube_sample, path, back_path in rotation.iterate_all_positions(cube):
            if self.match_pattern(cube_sample):
                # stop iterating, pattern matched!
                return cube_sample, path, back_path
        return None

    def match_pattern(self, cube):
        label_mapping = {}

        for face_name, face_pattern in self._pattern.iteritems():
            cube_face = cube.get_flat_face(face_name)
            for pattern_item, cube_item in izip(self.flat(face_pattern), cube_face):
                if pattern_item == 0: # skip this item
                    continue
                pattern_value = label_mapping.setdefault(pattern_item, cube_item)
                if pattern_value != cube_item:
                    return False
        return True

    # NOTE: workaround for numpy arrays
    @staticmethod
    def flat(obj):
        if hasattr(obj, 'flat'):
            return obj.flat
        else:
            return obj

    @classmethod
    def from_cube(cls, cube):
        return cls(cube.get_context())


class ExactCubePattern(CubePattern):
    def match_pattern(self, cube):
        for face_name, face_pattern in self._pattern.iteritems():
            cube_face = cube.get_flat_face(face_name)
            for pattern_item, cube_item in izip(self.flat(face_pattern), cube_face):
                if pattern_item == 0: # skip this item
                    continue
                if pattern_item != cube_item:
                    return False
        return True


class CubePatternWithAction(CubePattern):
 
    def __init__(self, pattern, coded_action):
        self._operations = cube_operation.parse_cube_notation(coded_action)
        super(CubePatternWithAction, self).__init__(pattern)
    
    def perform_action(self, cube):
        return cube_operation.perform_united_operations(cube, self._operations)

    def get_action(self):
        return self._operations


class ExactCubePatternWithAction(CubePatternWithAction, ExactCubePattern):
    pass


class StageError(Exception):
    pass


class SolveStage(object):
    
    final_pattern = None # when stage is finished
    stage_patterns = ()

    def __call__(self, cube):
        old_cube = cube
        final_match = self.final_pattern.check_at_all_positions(cube.copy())
        while final_match is None:
            for pattern in self.stage_patterns:
                match = pattern.check_at_all_positions(cube.copy())
                if match is not None:
                    old_cube = cube
                    cube, path = match
                    pattern.perform_action(cube)
                    # positioning
                    for x in path: yield x
                    # performing pattern
                    for x in pattern.get_action(): yield x
                    break
            if cube == old_cube:
                raise StageError("After all matching attempts, cube has not changed!")
            final_match = self.final_pattern.check_at_all_positions(cube.copy())

        final_cube, path = final_match
        for x in path: yield x

class SolvingProcess(object):
    
    stages = []

    def solve(self, cube):
        cube_copy = cube.copy()
        for stage in self.stages:
            for step in stage(cube_copy):
                yield step

