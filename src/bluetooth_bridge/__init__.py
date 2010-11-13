INBOX_ID = 1

OPCODES = {
    'vertical_turn': 1,
    'horizontal_turn': 2,
    'move': 3,
    'exit': 666,
}

class CommanderMeta(type):

    def __new__(cls, name, bases, attrs):
        for method_name, opcode in OPCODES.iteritems():
            attrs[method_name] = CommanderMeta._make_operation(opcode)
        return super(CommanderMeta, cls).__new__(cls, name, bases, attrs)

    @staticmethod
    def _make_operation(opcode):
        op_prefix = '%s:' % opcode
        def performer(self, *args):
            msg = op_prefix + ':'.join(str(a) for a in args) + ':'
            self.brick.message_write(self.inbox_id, msg)
        return performer


class Commander(object):

    __metaclass__ = CommanderMeta

    def __init__(self, brick, inbox_id=INBOX_ID):
        self.brick = brick
        self.inbox_id = INBOX_ID
        object.__init__(self)

