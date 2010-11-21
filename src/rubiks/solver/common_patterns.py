from rubiks import FaceType
from rubiks import solver
from rubiks.cube import NumpyCube as Cube

unpositioned_cross_pattern = solver.CubePattern({
        FaceType.DOWN: [ 0,  '2!', 0,
                        '2!','2!','2!',
                         0,  '2!', 0],
        })

cross_pattern = solver.CubePattern({
        FaceType.DOWN: [ 0,  '2!', 0,
                        '2!','2!','2!',
                         0,  '2!', 0],
        FaceType.RIGHT: [ 0, '6!', 0,
                          0, '6!', 0,
                          0,  0,   0],
        FaceType.FRONT: [ 0,   0,   0,
                         '3!','3!', 0,
                          0,   0,   0],
        FaceType.LEFT: [ 0,  0,   0,
                         0, '5!', 0,
                         0, '5!', 0],
        FaceType.BACK: [ 0,  0,   0,
                         0, '1!','1!',
                         0,  0,   0],
        })

first_layer_pattern = solver.CubePattern({
        FaceType.DOWN: ['2!','2!','2!',
                        '2!','2!','2!',
                        '2!','2!','2!'],
        FaceType.RIGHT: ['6!','6!','6!',
                         0,0,0,
                          0, 0, 0],
        FaceType.FRONT: ['3!',0, 0,
                         '3!',0, 0,
                         '3!',0, 0],
        FaceType.LEFT: [ 0, 0, 0,
                        0,0,0,
                        '5!','5!','5!'],
        FaceType.BACK: [ 0,0,'1!',
                         0,0,'1!',
                         0,0,'1!'],
        })

f2l_pattern = solver.CubePattern({
        FaceType.DOWN: ['2!','2!','2!',
                        '2!','2!','2!',
                        '2!','2!','2!'],
        FaceType.RIGHT: ['6!','6!','6!',
                         '6!','6!','6!',
                          0, 0, 0],
        FaceType.FRONT: ['3!','3!', 0,
                         '3!','3!', 0,
                         '3!','3!', 0],
        FaceType.LEFT: [ 0, 0, 0,
                        '5!','5!','5!',
                        '5!','5!','5!'],
        FaceType.BACK: [ 0,'1!','1!',
                         0,'1!','1!',
                         0,'1!','1!'],
        })

ll_cross_pattern = solver.CubePattern({
        FaceType.DOWN: ['2!','2!','2!',
                        '2!','2!','2!',
                        '2!','2!','2!'],
        FaceType.RIGHT: ['6!','6!','6!',
                         '6!','6!','6!',
                          0, 0, 0],
        FaceType.FRONT: ['3!','3!', 0,
                         '3!','3!', 0,
                         '3!','3!', 0],
        FaceType.LEFT: [ 0, 0, 0,
                        '5!','5!','5!',
                        '5!','5!','5!'],
        FaceType.BACK: [ 0,'1!','1!',
                         0,'1!','1!',
                         0,'1!','1!'],
        FaceType.UP:   [ 0,  '4!', 0,
                        '4!','4!','4!',
                         0,  '4!', 0],
        })

ll_face_pattern = solver.CubePattern({
        FaceType.DOWN: ['2!','2!','2!',
                        '2!','2!','2!',
                        '2!','2!','2!'],
        FaceType.RIGHT: ['6!','6!','6!',
                         '6!','6!','6!',
                          0, 0, 0],
        FaceType.FRONT: ['3!','3!', 0,
                         '3!','3!', 0,
                         '3!','3!', 0],
        FaceType.LEFT: [ 0, 0, 0,
                        '5!','5!','5!',
                        '5!','5!','5!'],
        FaceType.BACK: [ 0,'1!','1!',
                         0,'1!','1!',
                         0,'1!','1!'],
        FaceType.UP:   ['4!','4!','4!',
                        '4!','4!','4!',
                        '4!','4!','4!'],
        })

ll_except_side_pattern = solver.CubePattern({
        FaceType.DOWN: ['2!','2!','2!',
                        '2!','2!','2!',
                        '2!','2!','2!'],
        FaceType.RIGHT: ['6!','6!','6!',
                         '6!','6!','6!',
                         '6!', 0,  '6!'],
        FaceType.FRONT: ['3!','3!', 0,
                         '3!','3!', 0,
                         '3!','3!', 0],
        FaceType.LEFT: ['5!', 0,  '5!',
                        '5!','5!','5!',
                        '5!','5!','5!'],
        FaceType.BACK: ['1!','1!','1!',
                         0,  '1!','1!',
                        '1!','1!','1!'],
        FaceType.UP:   ['4!','4!','4!',
                        '4!','4!','4!',
                        '4!','4!','4!'],
        })

done_pattern = solver.CubePattern.from_cube(Cube.solved_cube())

