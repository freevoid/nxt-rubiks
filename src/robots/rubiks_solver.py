import time

import nxt

from bluetooth_bridge import Commander
from rubiks.cube import NumpyCube as Cube
from rubiks import FaceType

class RubiksRobot(object):

    COLOR_SENSOR_MOTOR_PORT = nxt.PORT_C
    PLATFORM_MOTOR_PORT = nxt.PORT_A
    HAND_MOTOR_PORT = nxt.PORT_B
    COLOR_SENSOR_PORT = nxt.PORT_2
    SONAR_PORT = nxt.PORT_1

    CUBE_CHECK_PERIOD = 1
    MAX_CUBE_PLACED_DISTANCE = 25
    ACCURATE_TURN_STRENGTH = 20

    def __init__(self, brick):
        self.brick = brick
        self.cmd = Commander(brick)

        self.platform_motor = nxt.Motor(brick, self.PLATFORM_MOTOR_PORT)
        self.hand_motor = nxt.Motor(brick, self.HAND_MOTOR_PORT)
        self.color_sensor_motor = nxt.Motor(brick, self.COLOR_SENSOR_MOTOR_PORT)
        self.color_sensor = nxt.Color20(brick, self.COLOR_SENSOR_PORT)
        self.sonar = nxt.Ultrasonic(brick, self.SONAR_PORT)

        self.motors = [self.hand_motor, self.platform_motor, self.color_sensor_motor]

        self._cs_angle_delta = 0

        self.idle_all()
        self.reset_rotation_counts()

    def reset_rotation_counts(self):
        for m in self.motors:
            m.reset_position(relative=False)
            m.reset_position(relative=True)

    def idle_all(self):
        for m in self.motors:
            m.idle()

    def is_cube_placed(self):
        return self.sonar.get_distance() < self.MAX_CUBE_PLACED_DISTANCE

    def wait_for_cube(self):
        '''
        Function returns as soon as cube is available
        '''
        while True:
            if self.is_cube_placed():
                return True
            time.sleep(self.CUBE_CHECK_PERIOD)

    def turn_platform(self, angle, accurate=True):
        strength = accurate and self.ACCURATE_TURN_STRENGTH or self.ACCURATE_TURN_STRENGTH*2
        self.cmd.horizontal_turn_ex(angle, strength)

    def turn_color_sensor(self, angle):
        self.cmd.camera_turn(angle, self.ACCURATE_TURN_STRENGTH)
        self._cs_angle_delta += angle

    def scan_face(self):
        return scan_cube_face(self)

    def get_color(self):
        return self.color_sensor.get_color()

    def remember_color_sensor(self):
        self._cs_angle_delta = 0

    def move_color_sensor_back(self):
        self.turn_color_sensor(-self._cs_angle_delta)


MOVE_TIME = 1.5

def scan_and_rotate(robot):
    for i in range(4):
        # TODO: check that platform is not moving
        yield robot.get_color()
        robot.turn_platform(90)
        time.sleep(MOVE_TIME)

def _scan_cube_face(robot):
    robot.remember_color_sensor()
    robot.turn_color_sensor(45) # move below center
    time.sleep(MOVE_TIME)
    # yield center cubie's color
    yield robot.get_color()
    robot.turn_color_sensor(35)
    for color in scan_and_rotate(robot):
        yield color
    robot.turn_color_sensor(-1)
    robot.turn_platform(45)
    time.sleep(MOVE_TIME)
    for color in scan_and_rotate(robot):
        yield color
    robot.turn_platform(-45)
    robot.move_color_sensor_back()

FACE_SCAN_MAPPING = {
    0: 4,
    1: 8,
    2: 1,
    3: 7,
    4: 0,
    5: 5,
    6: 3,
    7: 6,
    8: 2
}

def scan_cube_face(robot):
    raw_faces = list(_scan_cube_face(robot))
    face = [0]*9
    for (i, face_color) in enumerate(raw_faces):
        face[FACE_SCAN_MAPPING[i]] = face_color
    return face

def scan_cube(robot):
    c = Cube({})

    scan_n_set = lambda face_type:\
        c.set_face(face_type,
            c.face_from_label_list(list(scan_cube_face(robot))))

    scan_n_set(FaceType.UP)
    robot.cmd.vertical_turn()
    scan_n_set(FaceType.BACK)
    robot.cmd.vertical_turn()
    scan_n_set(FaceType.DOWN)
    robot.cmd.vertical_turn()
    scan_n_set(FaceType.FRONT)
    robot.cmd.vertical_turn()
    robot.turn_platform(-90)
    robot.cmd.vertical_turn()
    robot.turn_platform(-90)
    scan_n_set(FaceType.LEFT)
    robot.cmd.vertical_turn()
    robot.cmd.vertical_turn()
    scan_n_set(FaceType.RIGHT)
    robot.turn_platform(-90)
    robot.cmd.vertical_turn()
    robot.turn_platform(90)
    

