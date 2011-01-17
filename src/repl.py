import logging
logging.basicConfig(level=logging.DEBUG)

from robots.rubiks_solver import *

BRICK_HOST = '00:16:53:0D:17:8B'

if __name__=='__main__':
    import sys
    if len(sys.argv) > 1:
        r = RubiksRobot()
    else:
        r = RubiksRobot(BRICK_HOST)


