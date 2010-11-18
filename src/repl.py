import nxt

from bluetooth_bridge import Commander

BRICK_HOST = '00:16:53:0D:17:8B'

if __name__=='__main__':
    import sys
    if len(sys.argv) > 1:
        b = nxt.find_one_brick()
    else:
        b = nxt.find_one_brick(host=BRICK_HOST)

    c = Commander(b)

