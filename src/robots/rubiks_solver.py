import time
import logging

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
    ACCURATE_TURN_STRENGTH = 40
    SENSOR_TURN_STRENGTH = 20

    def __init__(self, brick_host=None):
        self.cmd = Commander(brick_finder=lambda: nxt.find_one_brick(host=brick_host))

        brick = self.cmd.brick
        self.platform_motor = nxt.Motor(brick, self.PLATFORM_MOTOR_PORT)
        self.hand_motor = nxt.Motor(brick, self.HAND_MOTOR_PORT)
        self.color_sensor_motor = nxt.Motor(brick, self.COLOR_SENSOR_MOTOR_PORT)
        self.color_sensor = nxt.Color20(brick, self.COLOR_SENSOR_PORT)
        self.sonar = nxt.Ultrasonic(brick, self.SONAR_PORT)

        self.motors = [self.hand_motor, self.platform_motor, self.color_sensor_motor]

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
        logging.info("TURN PLATFORM ISSUED: ANGLE %d" % angle)
        strength = accurate and self.ACCURATE_TURN_STRENGTH or self.ACCURATE_TURN_STRENGTH*2
        self.cmd.horizontal_turn_ex(angle, strength)

    def turn_color_sensor(self, angle):
        logging.info("TURN SENSOR   ISSUED: ANGLE %d" % angle)
        self.cmd.camera_turn(angle, self.SENSOR_TURN_STRENGTH)

    def scan_face(self):
        return scan_cube_face(self)

    def get_color(self):
        color = self.color_sensor.get_color()
        logging.info("GETTING COLOR: %d" % color)
        return color

    def move_color_sensor_at_start(self):
        try:
            self.color_sensor_motor.turn(-64, 360, timeout=0.05, brake=True)
        except nxt.BlockedException:
            pass

        self.color_sensor_motor.turn(5, 2, brake=True)
        time.sleep(0.4)
        self.color_sensor_motor.idle()
        self.cmd.reset_angles()

MOVE_TIME = 1.5

def scan_and_rotate(robot):
    for i in range(4):
        # TODO: check that platform is not moving
        yield robot.get_color()
        robot.turn_platform(90)

def _scan_cube_face(robot):
    robot.move_color_sensor_at_start()
    robot.turn_color_sensor(166) # move below center
    # yield center cubie's color
    yield robot.get_color()
    robot.turn_color_sensor(28)
    for color in scan_and_rotate(robot):
        yield color
    robot.turn_color_sensor(-4)
    robot.turn_platform(45)
    for color in scan_and_rotate(robot):
        yield color
    robot.turn_platform(-45)
    #robot.move_color_sensor_at_start()
    robot.turn_color_sensor(-90)

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

NXT_COLOR_MAPPING = {
    1: 6,
    2: 2,
    3: 1,
    4: 3,
    5: 5,
    6: 4,
}

def scan_cube_face(robot):
    raw_faces = list(_scan_cube_face(robot))
    face = [0]*9
    for (i, face_color) in enumerate(raw_faces):
        face[FACE_SCAN_MAPPING[i]] = face_color
    return face

def scan_cube(robot):
    c = Cube({})

    def scan_n_set(face_type):
        c.set_face(face_type,
            c.face_from_label_list(map(NXT_COLOR_MAPPING.get, scan_cube_face(robot))))
        logging.info("Scan completed for face %s. Cube:")
        logging.info("%s", c)

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

    return c

