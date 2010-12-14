import time

import nxt

from bluetooth_bridge import Commander

class RubiksRobot(object):

    COLOR_SENSOR_MOTOR_PORT = nxt.PORT_C
    PLATFORM_MOTOR_PORT = nxt.PORT_A
    HAND_MOTOR_PORT = nxt.PORT_B
    COLOR_SENSOR_PORT = nxt.PORT_2
    SONAR_PORT = nxt.PORT_1

    CUBE_CHECK_PERIOD = 1
    MAX_CUBE_PLACED_DISTANCE = 25

    def __init__(self, brick):
        self.brick = brick
        self.cmd = Commander(brick)

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

