INBOX_ID = 1

OPCODES = {
    'vertical_turn': 1,
    'horizontal_turn': 2,
    'move': 3,
    'exit': 666,
}

class Commander(object):
    def __init__(self, brick, inbox_id=INBOX_ID):
        self.brick = brick
        self.inbox_id = INBOX_ID
        object.__init__(self)

    def __getattribute__(self, attrname):
        if attrname != 'operation' and attrname in OPCODES:
            return self.operation(OPCODES[attrname])
        else:
            return super(Commander, self).__getattribute__(attrname)

    def operation(self, opcode):
        op_prefix = '%s:' % opcode
        def performer(*args):
            msg = op_prefix + ':'.join(str(a) for a in args) + ':'
            self.brick.message_write(self.inbox_id, msg)
        return performer

