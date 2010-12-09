from rubiks import FaceType
from rubiks import solver
from rubiks.actions import make_cube_action
from rubiks.solver import common_patterns

class UnpositionedCross(solver.SolveStage):
    
    final_pattern = common_patterns.unpositioned_cross_pattern

    safe_action = staticmethod(make_cube_action("D"))

    stage_patterns = map(lambda args: solver.CubePatternWithOperationPath(*args),
        (({
            FaceType.DOWN:
                [0,0,0,
                0,'2!','-2!',
                0,0,0],
            FaceType.FRONT:
                [0,0,0,
                '2!',0,0,
                0,0,0]
        }, "FD'LD"),
        ({
            FaceType.DOWN:
                [0,0,0,
                0,'2!','-2!',
                0,0,0],
            FaceType.FRONT:
                [0,'2!',0,
                0,0,0,
                0,0,0]
         }, "D'LD"),
        ({
            FaceType.DOWN:
                [0,0,0,
                0,'2!','-2!',
                0,0,0],
            FaceType.LEFT:
                [0,0,0,
                0,0,'2!',
                0,0,0]
         }, "F'"),
        ({
            FaceType.DOWN:
                [0,0,0,
                0,'2!','-2!',
                0,0,0],
            FaceType.FRONT:
                [0,0,0,
                0,0,'2!',
                0,0,0]
         }, "FDR'D'"),
        ({
            FaceType.DOWN:
                [0,0,0,
                0,'2!','-2!',
                0,0,0],
            FaceType.UP:
                [0,0,0,
                '2!',0,0,
                0,0,0]
         }, "F2"),
        ({
            FaceType.DOWN:
                [0,0,0,
                0,'2!','-2!',
                0,0,0],
            FaceType.FRONT:
                [0,0,0,
                0,0,0,
                0,'2!',0]
         }, "DR'D'"),
        ))


class PositionCross(solver.SolveStage):
    
    final_pattern = common_patterns.cross_pattern

    stage_patterns = map(lambda args: solver.CubePatternWithOperationPath(*args),
        (
         ({
            FaceType.DOWN:
                [0,0,0,
                0,'2!',0,
                0,0,0],
            FaceType.FRONT:
                [0,0,0,
                0,1,1,
                0,0,0],
            FaceType.UP:
                [0,0,0,
                '2!',0,0,
                0,0,0]
         }, "F2"),
         ({
            FaceType.DOWN:
                [0,0,0,
                0,'2!',0,
                0,0,0],
            FaceType.FRONT:
                [0,0,0,
                0,-1,1,
                0,0,0],
            FaceType.UP:
                [0,0,0,
                '2!',0,0,
                0,0,0],
            FaceType.LEFT:
                [0,0,0,
                0,1,0,
                0,0,0],
         }, "U"),
         ({
            FaceType.DOWN:
                [0,0,0,
                0,'2!',0,
                0,0,0],
            FaceType.FRONT:
                [0,0,0,
                0,-1,1,
                0,0,0],
            FaceType.UP:
                [0,0,0,
                '2!',0,0,
                0,0,0],
            FaceType.BACK:
                [0,0,0,
                0,1,0,
                0,0,0],
         }, "U2"),
         ({
            FaceType.DOWN:
                [0,0,0,
                0,'2!',0,
                0,0,0],
            FaceType.FRONT:
                [0,0,0,
                0,-1,1,
                0,0,0],
            FaceType.UP:
                [0,0,0,
                '2!',0,0,
                0,0,0],
            FaceType.RIGHT:
                [0,0,0,
                0,1,0,
                0,0,0],
         }, "U'"),
         ({
            FaceType.DOWN:
                [0,'2!',0,
                '2!','2!','2!',
                0,'2!',0],
            FaceType.FRONT:
                [0,0,0,
                -1,1,0,
                0,0,0]

         }, "F2"),
        ))


class DownCorners(solver.SolveStage):
    
    final_pattern = common_patterns.first_layer_pattern

    base_pattern = {
        FaceType.DOWN:
            [0,'2!',0,
            '2!','2!','2!',
            0,'2!',0],
        FaceType.RIGHT: [0, 6, 0,
                         0, 6, 0,
                         0, 0, 0],
        FaceType.FRONT: [0, 0, 0,
                         3, 3, 0,
                         0, 0, 0],
        FaceType.LEFT: [ 0, 0, 0,
                         0, 5, 0,
                         0, 5, 0],
        FaceType.BACK: [ 0, 0, 0,
                         0, 1, 1,
                         0, 0, 0],
        }

    stage_patterns = [
        solver.CubePatternWithOperationPath.inherited(base_pattern, pattern, path) for pattern, path in
        (
         # after positioning
         # target on left
         ({
            FaceType.LEFT: [0,0,'2!',0,5,0,0,5,0],
            FaceType.FRONT: [0,0,3,3,3,0,0,0,0],
            FaceType.UP: [5,0,0,0,0,0,0,0,0],
          }, "L'U'L"),
         # target on up 
         ({
            FaceType.LEFT: [0,0,3,0,5,0,0,5,0],
            FaceType.FRONT: [0,0,5,3,3,0,0,0,0],
            FaceType.UP: ['2!',0,0,0,0,0,0,0,0],
          }, "FU2F'U'FUF'"),
         # target on front
         ({
            FaceType.LEFT: [0,0,5,0,5,0,0,5,0],
            FaceType.FRONT: [0,0,'2!',3,3,0,0,0,0],
            FaceType.UP: [3,0,0,0,0,0,0,0,0],
          }, "FUF'"),
         # positioning of corner cubies
         # when target 2! is on left
         ({
            FaceType.LEFT: [0,0,'2!',0,5,0,0,5,0],
            FaceType.FRONT: [0,0,6,3,3,0,0,0,0],
            FaceType.UP: [3,0,0,0,0,0,0,0,0],
          }, "U'"),
         ({
            FaceType.LEFT: [0,0,'2!',0,5,0,0,5,0],
            FaceType.FRONT: [0,0,5,3,3,0,0,0,0],
            FaceType.UP: [1,0,0,0,0,0,0,0,0],
          }, "U"),
         ({
            FaceType.LEFT: [0,0,'2!',0,5,0,0,5,0],
            FaceType.FRONT: [0,0,1,3,3,0,0,0,0],
            FaceType.UP: [6,0,0,0,0,0,0,0,0],
          }, "U2"),
         # when target 2! is on up
         ({
            FaceType.LEFT: [0,0,5,0,5,0,0,5,0],
            FaceType.FRONT: [0,0,1,3,3,0,0,0,0],
            FaceType.UP: ['2!',0,0,0,0,0,0,0,0],
          }, "U"),
         ({
            FaceType.LEFT: [0,0,1,0,5,0,0,5,0],
            FaceType.FRONT: [0,0,6,3,3,0,0,0,0],
            FaceType.UP: ['2!',0,0,0,0,0,0,0,0],
          }, "U2"),
         ({
            FaceType.LEFT: [0,0,6,0,5,0,0,5,0],
            FaceType.FRONT: [0,0,3,3,3,0,0,0,0],
            FaceType.UP: ['2!',0,0,0,0,0,0,0,0],
          }, "U'"),
         # when target 2! is on front
         ({
            FaceType.LEFT: [0,0,3,0,5,0,0,5,0],
            FaceType.FRONT: [0,0,'2!',3,3,0,0,0,0],
            FaceType.UP: [6,0,0,0,0,0,0,0,0],
          }, "U'"),
         ({
            FaceType.LEFT: [0,0,6,0,5,0,0,5,0],
            FaceType.FRONT: [0,0,'2!',3,3,0,0,0,0],
            FaceType.UP: [1,0,0,0,0,0,0,0,0],
          }, "U2"),
         ({
            FaceType.LEFT: [0,0,1,0,5,0,0,5,0],
            FaceType.FRONT: [0,0,'2!',3,3,0,0,0,0],
            FaceType.UP: [5,0,0,0,0,0,0,0,0],
          }, "U"),
         # moves to pick wrong cubie from down corner
         ({
            FaceType.FRONT: ['2!',0,0,3,3,0,0,0,0],
         }, "FUF'"),
         ({
            FaceType.LEFT: [0,0,0,0,5,0,0,5,'2!'],
         }, "FUF'"),
         ({
            FaceType.DOWN: [0,'2!','2!','2!','2!','2!',0,'2!',0],
            FaceType.LEFT: [0,0,0,0,5,0,0,5,-5],
            FaceType.FRONT: [-3,0,0,3,3,0,0,0,0],
         }, "FUF'"),
        )
    ]


class MiddleSideBlocks(solver.SolveStage):
    
    final_pattern = common_patterns.f2l_pattern

    base_pattern = {
        FaceType.DOWN: (2,)*9,
        FaceType.UP: (0,0,0,
                      0,4,0,
                      0,0,0),
        FaceType.RIGHT: [6, 6, 6,
                         0, 6, 0,
                         0, 0, 0],
        FaceType.FRONT: [3, 0, 0,
                         3, 3, 0,
                         3, 0, 0],
        FaceType.LEFT: [ 0, 0, 0,
                         0, 5, 0,
                         5, 5, 5],
        FaceType.BACK: [ 0, 0, 1,
                         0, 1, 1,
                         0, 0, 1],
        }

    stage_patterns = [
        solver.CubePatternWithOperationPath.inherited(base_pattern, pattern, path) for pattern, path in
        (
         # place positioned cubie
         ({
            FaceType.FRONT: [3, 0, 0,
                             3, 3, 3,
                             3, 0, 0],
            FaceType.UP: (0,0,0,
                          6,4,0,
                          0,0,0),
          }, "URUR'U'F'U'F"),
         ({
            FaceType.UP: (0,0,0,
                          0,4,0,
                          0,3,0),
            FaceType.RIGHT: [6, 6, 6,
                             0, 6, 0,
                             0, 6, 0],
          }, "U'F'U'FURUR'"),
         # position cubie
         ({
            FaceType.UP: (0,0,0,
                          -4,4,0,
                          0,0,0),
            FaceType.FRONT: [3, 0, 0,
                             3, 3, 6,
                             3, 0, 0],
          }, "U'"),
         ({
            FaceType.UP: (0,0,0,
                          -4,4,0,
                          0,0,0),
            FaceType.FRONT: [3, 0, 0,
                             3, 3, 1,
                             3, 0, 0],
          }, "U2"),
         ({
            FaceType.UP: (0,0,0,
                          -4,4,0,
                          0,0,0),
            FaceType.FRONT: [3, 0, 0,
                             3, 3, 5,
                             3, 0, 0],
          }, "U"),
         # pick wrong cubie
         ({
            FaceType.FRONT: [3, 0, 0,
                             3, 3, 0,
                             3, '-3', 0],
            FaceType.RIGHT: [6, 6, 6,
                             0, 6, '-6',
                             0, 0, 0],
          }, "U'F'U'FURUR'"),
         ({
            FaceType.FRONT: [3, 0, 0,
                             3, 3, 0,
                             3, -3, 0],
            FaceType.RIGHT: [6, 6, 6,
                             0, 6, 6,
                             0, 0, 0],
          }, "U'F'U'FURUR'"),
         ({
            FaceType.FRONT: [3, 0, 0,
                             3, 3, 0,
                             3, 3, 0],
            FaceType.RIGHT: [6, 6, 6,
                             0, 6, -6,
                             0, 0, 0],
          }, "U'F'U'FURUR'"),
        )]


class CrossOnLastLayer(solver.SolveStage):
    
    final_pattern = common_patterns.ll_cross_pattern

    base_pattern = {
        FaceType.DOWN: (2,)*9,
        FaceType.UP: (0,0,0,
                      0,4,0,
                      0,0,0),
        FaceType.RIGHT: [6, 6, 6,
                         6, 6, 6,
                         0, 0, 0],
        FaceType.FRONT: [3, 3, 0,
                         3, 3, 0,
                         3, 3, 0],
        FaceType.LEFT: [ 0, 0, 0,
                         5, 5, 5,
                         5, 5, 5],
        FaceType.BACK: [ 0, 1, 1,
                         0, 1, 1,
                         0, 1, 1],
        }

    stage_patterns = [
        solver.CubePatternWithOperationPath.inherited(base_pattern, pattern, path) for pattern, path in
        (
         ({
            FaceType.UP: (0,4,0,
                          -4,4,4,
                          0,-4,0),
          }, "FURU'R'F'"),
         # any other case
         ({}, "FRUR'U'F'"),
        )]


class FaceOnLastLayer(solver.SolveStage):
    
    final_pattern = common_patterns.ll_face_pattern

    base_pattern = CrossOnLastLayer.base_pattern.copy()

    stage_patterns = [
        solver.CubePatternWithOperationPath.inherited(base_pattern, pattern, path) for pattern, path in
        (
         # place positioned cubie
         ({
            FaceType.UP: (0,4,4,
                          4,4,4,
                          0,4,4),
            FaceType.FRONT: (0,0,4,
                          0,0,0,
                          0,0,4),
          }, "R2DR'U2RD'R'U2R'"),
         ({
            FaceType.UP: (4,4,4,
                          4,4,4,
                          0,4,0),
            FaceType.FRONT: (0,0,0,
                          0,0,0,
                          0,0,4),
            FaceType.BACK: (0,0,0,
                          0,0,0,
                          4,0,0),
          }, "R'F'LFRF'L'F"),
         ({
            FaceType.UP: (0,4,4,
                          4,4,4,
                          4,4,0),
            FaceType.LEFT: (0,0,4,
                          0,0,0,
                          0,0,0),
            FaceType.BACK: (0,0,0,
                          0,0,0,
                          4,0,0),
          }, "R'F'L'FRF'LF"),
         ({
            FaceType.UP: (4,4,0,
                          4,4,4,
                          0,4,0),
            FaceType.FRONT: (0,0,0,
                          0,0,0,
                          0,0,4),
            FaceType.RIGHT: (0,0,0,
                          0,0,0,
                          4,0,0),
            FaceType.BACK: (4,0,0,
                          0,0,0,
                          0,0,0),
          }, "RUR'URU2R'"),
         ({
            FaceType.UP: (0,4,0,
                          4,4,4,
                          0,4,4),
            FaceType.FRONT: (0,0,4,
                          0,0,0,
                          0,0,0),
            FaceType.RIGHT: (0,0,0,
                          0,0,0,
                          0,0,4),
            FaceType.LEFT: (4,0,0,
                          0,0,0,
                          0,0,0),
          }, "RU2R'U'RU'R'"),
         ({
            FaceType.UP: (0,4,0,
                          4,4,4,
                          0,4,0),
            FaceType.FRONT: (0,0,0,
                          0,0,0,
                          0,0,4),
            FaceType.LEFT: (4,0,4,
                          0,0,0,
                          0,0,0),
            FaceType.BACK: (0,0,0,
                          0,0,0,
                          4,0,0),
          }, "RU2R2U'R2U'R2U'R"),
         ({
            FaceType.UP: (0,4,0,
                          4,4,4,
                          0,4,0),
            FaceType.FRONT: (0,0,4,
                          0,0,0,
                          0,0,4),
            FaceType.BACK: (4,0,0,
                          0,0,0,
                          4,0,0),
          }, "FRUR'U'RUR'U'RUR'U'F'"),
        )]


class PositionLLCorners(solver.SolveStage):
    
    final_pattern = common_patterns.ll_except_side_pattern

    safe_action = staticmethod(make_cube_action("U"))

    base_pattern = CrossOnLastLayer.base_pattern.copy()
    base_pattern.update({
        FaceType.UP: (4,)*9,
        })

    stage_patterns = [
        solver.CubePatternWithOperationPath.inherited(base_pattern, pattern, path) for pattern, path in
        (
         # place positioned cubie
         ({
            FaceType.FRONT: [0, 0, 3,
                             0, 3, 0,
                             0, 0, 0],
            FaceType.BACK: (1,0,0,
                          0,1,0,
                          0,0,0),
            FaceType.LEFT: (5,0,5,
                          0,5,0,
                          0,0,0),
          }, "RU2R'U'RU2L'UR'U2"),
         ({
            FaceType.FRONT: [0, 0, 0,
                             0, 3, 0,
                             0, 0, 3],
            FaceType.BACK: (1,0,0,
                          0,1,0,
                          0,0,0),
            FaceType.LEFT: (5,0,0,
                          0,5,0,
                          0,0,0),
            FaceType.RIGHT: (0,0,0,
                          0,6,0,
                          0,0,6),
          }, "L'URU'LUL'UR'U'LU2RU2R'"),
        )]


class SideOnLastLayer(solver.SolveStage):
    
    final_pattern = common_patterns.done_pattern

    base_pattern = {
        FaceType.DOWN: (2,)*9,
        FaceType.UP: (0,0,0,
                      0,4,0,
                      0,0,0),
        FaceType.RIGHT: [6, 6, 6,
                         6, 6, 6,
                         0, 0, 0],
        FaceType.FRONT: [3, 3, 0,
                         3, 3, 0,
                         3, 3, 0],
        FaceType.LEFT: [ 0, 0, 0,
                         5, 5, 5,
                         5, 5, 5],
        FaceType.BACK: [ 0, 1, 1,
                         0, 1, 1,
                         0, 1, 1],
        }

    stage_patterns = [
        solver.CubePatternWithOperationPath.inherited(base_pattern, pattern, path) for pattern, path in
        (
         # place positioned cubie
         ({
            FaceType.FRONT: [3, 0, 0,
                             3, 3, 3,
                             3, 0, 0],
            FaceType.UP: (0,0,0,
                          6,4,0,
                          0,0,0),
          }, "URUR'U'F'U'F"),
        )]


class SimplestSolver(solver.SolvingProcess):
    
    stages = (UnpositionedCross(), PositionCross(), DownCorners(),
            MiddleSideBlocks(),
            CrossOnLastLayer(),
            FaceOnLastLayer(),
            PositionLLCorners(),
            SideOnLastLayer(),
            )

