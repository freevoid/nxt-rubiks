from rubiks import FaceType
from rubiks.cube import NumpyCube as Cube
from rubiks import solver
from rubiks.solver.common_patterns import cross_pattern, f2l_pattern, done_pattern

class Cross(solver.SolveStage):
    final_pattern = cross_pattern

class F2L(solver.SolveStage):
    final_pattern = f2l_pattern

class LL(solver.SolveStage):
    final_pattern = done_pattern

class FridrichSolver(solver.SolvingProcess):
    stages = (Cross(), F2L(), LL())

