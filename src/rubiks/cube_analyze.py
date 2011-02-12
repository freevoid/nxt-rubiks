from rubiks import FaceType
from rubiks.focus import focus_on_face
from rubiks import solver

position_cube_pattern = solver.CubePattern({
        FaceType.BACK: [0, 0, 0,
                        0, '1!', 0,
                        0, 0, 0],
        FaceType.DOWN: [0, 0, 0,
                        0, '2!', 0,
                        0, 0, 0],
        })

def detect_centers(cube_with_mailformed_centers):
    match = position_cube_pattern.check_at_all_positions(
                cube_with_mailformed_centers)
    if match is None:
        raise ValueError("Color codes with 1 and 2 are mailformed")
    else:
        positioned_cube, path = match
        # fix centers
        for bound_color_id, face_id in  FaceType.ENUMERATED_FACES:
            face = positioned_cube.get_face(face_id)
            face[1][1] = bound_color_id
        return positioned_cube

