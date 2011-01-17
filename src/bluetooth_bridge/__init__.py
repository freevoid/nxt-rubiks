import os
import tempfile

from nxt.error import DirProtError

import nxt_push

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

INBOX_ID = 1
OUTBOX_ID = 10

# format: METHOD_NAME: (OPCODE, ARGUMENT_AMOUNT)
OPCODES = {
    'vertical_turn': (1, 0),
    'horizontal_turn': (2, 1),
    'move': (3, 3),
    'configure_hturn': (4, 2),
    'horizontal_turn_ex': (5, 2),
    'camera_turn': (6, 2),
    'reset_angles': (7, 0),
    'configure_vturn': (8, 2),
    'exit': (666, 0),
}

class CommanderMeta(type):

    def __new__(cls, name, bases, attrs):
        for method_name, opcode in OPCODES.iteritems():
            attrs[method_name] = CommanderMeta._make_operation(opcode)
        return super(CommanderMeta, cls).__new__(cls, name, bases, attrs)

    @staticmethod
    def _make_operation((opcode, argcount)):
        #op_prefix = '%s:' % opcode
        def performer(self, *args):
            if len(args) != argcount:
                raise ValueError("Operation expected exactly %d arguments" % argcount)
            
            # critical section
            cmdid = self._cmdid
            self._cmdid += 1

            cmd_sequence = (opcode, cmdid) + args
            msg = ':'.join(map(str, cmd_sequence)) + ':'
            self.brick.message_write(self.inbox_id, msg)
            return self.wait_result(cmdid)

        return performer


class Commander(object):

    __metaclass__ = CommanderMeta

    _cmdid = 1

    program_name = 'bt_bridge'

    def __init__(self, brick_finder, inbox_id=INBOX_ID, outbox_id=OUTBOX_ID):
        self.brick = brick_finder()
        self.brick_finder = brick_finder
        self.inbox_id = inbox_id
        self.outbox_id = outbox_id
        object.__init__(self)

    def wait_result(self, cmdid):
        okay = False
        while True:
            try:
                status, message = self.brick.message_read(self.outbox_id, 0, True)
                id = int(message[:-1])
                if cmdid != id:
                    print "GOT ID, BUT IT DOESN'T MATCH:", id, cmdid
                    continue
                else:
                    okay = True
                    break
            except DirProtError:
                continue
        return okay

    def reload_program(self):
        try:
            self.brick.stop_program()
        except DirProtError:
            pass # program is not running
        compiled_program_path = self.recompile_program()
        nxt_push.write_file(self.brick, compiled_program_path)
        self.start_program()

    def start_program(self):
        self.brick.start_program('%s.rxe' % self.program_name)

    def get_program_path(self):
        return os.path.join(
            MODULE_DIR,
            self.program_name + '.nxc')

    def recompile_program(self):
        nxc_path = self.get_program_path()
        nxc_dir = os.path.dirname(nxc_path)
        tmpfile = os.path.join(tempfile.gettempdir(), self.program_name + '.rxe')
        os.system('nbc "%s" -I="%s" -O="%s"' % (nxc_path, nxc_dir, tmpfile))
        return tmpfile

