from rubiks import FaceType
from rubiks.cube import NumpyCube as Cube
from rubiks import solver

cross_pattern = solver.ExactCubePattern({
        FaceType.DOWN: [0,2,0,
                        2,2,2,
                        0,2,0],
        FaceType.RIGHT: [0,6,0,
                         0,6,0,
                         0,0,0],
        FaceType.FRONT: [0,0,0,
                         3,3,0,
                         0,0,0],
        FaceType.LEFT: [0,0,0,
                        0,5,0,
                        0,5,0],
        FaceType.BACK: [0,0,0,
                        0,1,1,
                        0,0,0],
        })

f2l_pattern = solver.ExactCubePattern({
        FaceType.DOWN: [0,2,0,
                        2,2,2,
                        0,2,0],
        FaceType.RIGHT: [6,6,6,
                         6,6,6,
                         0,0,0],
        FaceType.FRONT: [3,3,0,
                         3,3,0,
                         3,3,0],
        FaceType.LEFT: [0,0,0,
                        5,5,5,
                        5,5,5],
        FaceType.BACK: [0,1,1,
                        0,1,1,
                        0,1,1],
        })

done_pattern = solver.CubePattern.from_cube(Cube.solved_cube())


class Cross(solver.SolveStage):
    final_pattern = cross_pattern

class F2L(solver.SolveStage):
    final_pattern = f2l_pattern

class LL(solver.SolveStage):
    final_pattern = done_pattern

class FridrichSolver(solver.SolvingProcess):
    stages = (Cross(), F2L(), LL())

