import nxt

BRICK_HOST = '00:16:53:0D:17:8B'

if __name__=='__main__':
    b = nxt.find_one_brick(host=BRICK_HOST)

