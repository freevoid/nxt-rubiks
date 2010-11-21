from rubiks import cube_operation
from rubiks import rotation

def make_cube_action(coded_op):
    parsed = list(cube_operation.parse_cube_notation(coded_op))
    def action(cube):
        cube_operation.perform_united_operations(cube, parsed)
        return parsed
    return action

def chain_actions(*actions):
    def chained(cube):
        for action in actions:
            for x in action(cube):
                yield x
    return chained

def make_action_from_rotation_path(path):
    unified_path = map(cube_operation.tag_rotation, path)
    def rotation_action(cube):
        rotation.rotate_path(cube, path)
        return unified_path
    return rotation_action

def prepend_rotation_path_to_action(path, action):
    return chain_actions(
            make_action_from_rotation_path(path),
            action)
