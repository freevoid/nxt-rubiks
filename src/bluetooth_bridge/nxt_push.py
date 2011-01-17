import sys
from nxt.brick import FileWriter
from nxt.error import FileNotFound

def _write_file(b, fname, data):
    w = FileWriter(b, fname, len(data))
    print 'Pushing %s (%d bytes) ...' % (fname, w.size),
    sys.stdout.flush()
    w.write(data)
    print 'wrote %d bytes' % len(data)
    w.close()

def write_file(b, fname):
    f = open(fname)
    data = f.read()
    f.close()
    try:
        b.delete(fname)
        print 'Overwriting %s on NXT' % fname
    except FileNotFound:
        pass
    _write_file(b, fname, data)

