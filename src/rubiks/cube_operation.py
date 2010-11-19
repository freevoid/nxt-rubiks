import re

from rubiks import RotationType, FaceType
from rubiks.rotation import rotate
from rubiks.face_turn import perform_face_turn

CUBE_ROTATION = 'cube_rotation'
CUBE_FACE_TURN = 'cube_face_turn'

OPERATION_TYPE_MAP = {
    CUBE_ROTATION: rotate,
    CUBE_FACE_TURN: perform_face_turn,
}

NOTATION_TOKEN = re.compile(r"B'|B2|B|D'|D2|D|F'|F2|F|U'|U2|U|L'|L2|L|R'|R2|R|x'|x2|x|y'|y2|y|z'|z2|z")

def parse_cube_notation(coded_operations):
    for re_match in NOTATION_TOKEN.finditer(coded_operations):
        op_token = re_match.group()
        if len(op_token) == 2:
            type_, subtype = op_token
            if subtype == '2':
                direction = RotationType.DOUBLE_ROTATE
            elif subtype == "'":
                direction = RotationType.ANTICLOCKWISE
            else:
                raise ValueError("Unexpected subtype: \"%s\"" % subtype)
        elif len(op_token) == 1:
            type_ = op_token
            direction = RotationType.CLOCKWISE
        else:
            raise ValueError("Unexpected token length: %s" % op_token)
        
        # for now we have a direction and type_ in scope
        if type_ in FaceType.FACES:
            yield (CUBE_FACE_TURN, (type_, direction))
        elif type_ in ('x', 'y', 'z'):
            yield (CUBE_ROTATION, (type_.upper(), direction))
        else:
            raise ValueError("Unexpected token type: %s" % type_)

def perform_united_operation(cube, op_type, op_parameters):
    op = OPERATION_TYPE_MAP.get(op_type)
    if op is None:
        raise ValueError("Unknown cube operation type: %s" % op)
    else:
        cube = op(cube, op_parameters)
    return cube

def perform_united_operations(cube, op_path):
    for op_type, op_parameters in op_path:
        cube = perform_united_operation(cube, op_type, op_parameters)
    return cube

def perform_coded_operations(cube, coded_operations):
    return perform_united_operations(cube,
            parse_cube_notation(coded_operations))

