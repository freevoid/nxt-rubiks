from itertools import izip

from rubiks import FaceType, RotationType
from rubiks import rotation
from rubiks import cube_operation
from rubiks.actions import prepend_rotation_path_to_action
from rubiks.cube import NumpyCube as Cube

make_face = Cube.face_from_label_list

__all__ = ('CubePattern', 'CubePatternWithAction',
        'CubePatternWithOperationPath', 'SolveStage', 'SolvingProcess')

class CubePattern(object):
    '''
    Flexible cube pattern format:

    Pattern given as hash that maps face to face pattern.
    Each face pattern is just a python list/tuple of marks, length of 9,
    for each element in face. Marks have following format:

    * 0 or '0': checking is passed for this element;

    * positive int or string, representing it: element is matched if all previous
    positions with same mark at target cube were with the same code. Thus,
    this int is not a code of cube element, but maps to this code on first
    occassion;

    * negative int or string, representing it: same as above, but element is
    matched if and only if corresponding cube code is not equals;

    * string representing one of previous two codes but with '!' at the end:
    Do exact match with corresponding cube element. Do not use a mapping.
    
    '''

    def __init__(self, pattern, verbosity=0):
        self._pattern = pattern
        self.verbosity = verbosity
        super(CubePattern, self).__init__()

    @classmethod
    def inherited(cls, parent_pattern, child_pattern, *args, **kwargs):
        obj = cls(parent_pattern.copy(), *args, **kwargs)
        obj._pattern.update(child_pattern)
        return obj

    def check_at_all_positions(self, cube):
        '''
        Check pattern for all possible rotations of cube.

        Return tuple of (matched_cube, path_to_rotate_to_match).
        Return None if no match is found.

        Original cube stays unchanged.
        '''
        for cube_sample, path, back_path in rotation.iterate_all_positions(cube.copy()):
            if self.match_pattern(cube_sample):
                # stop iterating, pattern matched!
                return cube_sample, path
        return None

    def match_pattern(self, cube):
        '''
        Return True if pattern match given cube else return False.
        Cube stays unchanged.
        '''
        label_mapping = {}
        negative_label_mapping = {}

        if self.verbosity: print "PATTERN MATCHING!"
        for face_name, face_pattern in self._pattern.iteritems():
            cube_face = list(cube.get_flat_face(face_name))
            if self.verbosity: print "CHECKING FACE", cube_face
            for pattern_item, cube_item in izip(self.flat(face_pattern), cube_face):
                if self.verbosity: print "PATTERN:", pattern_item, "CUBE:", cube_item, "LOCAL MAPPING:", label_mapping, "BLACKLIST:", negative_label_mapping
                if pattern_item == 0 or pattern_item == '0': # skip this item
                    continue

                pattern_item = str(pattern_item)
                negative = True if pattern_item.startswith('-') else False
                force = True if pattern_item.endswith('!') else False
                pattern_item_value = int(pattern_item.strip('-!'))

                if self.verbosity: print "NEGATIVE:", negative, "FORCE:", force, "PIVALUE:", pattern_item_value

                if force:
                    pattern_value = pattern_item_value
                else:
                    pattern_value = label_mapping.get(pattern_item_value)
                    if pattern_value is None:
                        if negative:
                            if self.verbosity: print "APPENDING", cube_item, "TO BLACKLIST FOR ITEM", pattern_item_value
                            blacklist = negative_label_mapping.setdefault(pattern_item_value, [])
                            blacklist.append(cube_item)
                            continue
                        else:
                            label_mapping[pattern_item_value] = pattern_value = cube_item
                            blacklist = negative_label_mapping.get(pattern_item_value, [])
                            if self.verbosity: print "CHECKING BLACKLIST FOR ITEM", pattern_item, ":", blacklist
                            if pattern_value in blacklist:
                                return False
                    elif not negative:
                        blacklist = negative_label_mapping.get(pattern_item_value, [])
                        if self.verbosity: print "CHECKING BLACKLIST FOR ITEM", pattern_item, ":", blacklist
                        if pattern_value in blacklist:
                            return False

                if self.verbosity: print "PATTERN_VALUE:", pattern_value
                if (pattern_value != cube_item and not negative)\
                        or (pattern_value == cube_item and negative):
                    if self.verbosity: print "RETURNS FALSE!!!"
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


class CubePatternWithAction(CubePattern):
 
    def __init__(self, pattern, action):
        self._action = action
        super(CubePatternWithAction, self).__init__(pattern)
    
    def perform_action(self, cube):
        return self._action(cube)

    def get_action(self):
        return self._action


class CubePatternWithOperationPath(CubePatternWithAction):

    def __init__(self, pattern, coded_operation):
        # save operations because we want to iterate them more than once
        operations = list(cube_operation.parse_cube_notation(coded_operation))
        def action(cube):
            cube_operation.perform_united_operations(cube, operations)
            return operations

        super(CubePatternWithOperationPath, self).__init__(pattern, action)


class StageError(Exception):
    pass


class SolveStage(object):
    
    final_pattern = None # when stage is finished
    stage_patterns = ()
    safe_action = None

    verbosity = 0

    def __call__(self, cube):
        final_match = self.final_pattern.check_at_all_positions(cube)
        while final_match is None:
            action = self.choose_stage_action(cube)
            old_cube = cube.copy()
            if self.verbosity: print "Cube before action:"; print old_cube
            # performing action, changing cube
            action_path = action(cube)
            # yielding path that we used to perform pattern
            for x in action_path: yield x
            if self.verbosity: print "Cube after action:"; print cube

            if cube == old_cube:
                raise StageError("After stage action cube has not changed!", cube.copy())

            final_match = self.final_pattern.check_at_all_positions(cube)

        final_cube, path = final_match
        #for x in path: yield cube_operation.tag_rotation(x)

    def choose_stage_action(self, cube):
        '''
        Returns two callables representing action
        Cube stays unchanged.
        '''
        for pattern in self.stage_patterns:
            if self.verbosity: print "Checking pattern:", pattern._pattern
            match = pattern.check_at_all_positions(cube)
            if self.verbosity: print "Match:", match
            if match is not None:
                matched_cube, path_to_match = match
                return prepend_rotation_path_to_action(path_to_match,
                        pattern.perform_action)
        if self.safe_action is not None:
            return self.safe_action
        else:
            raise StageError("No match found for cube and there is no safe_action for stage!", cube.copy())


class SolvingProcess(object):
    
    stages = []

    def solve(self, cube):
        cube_copy = cube.copy()
        for stage in self.stages:
            print "STAGE %s" % stage.__class__.__name__
            for step in stage(cube_copy):
                print 'yielding', step
                yield step
            print "AFTER STAGE %s WE GOT CUBE:" % stage.__class__.__name__
            print cube_copy

    __call__ = solve

