from google.protobuf.message import Message
from google.protobuf.descriptor import FieldDescriptor, Descriptor



# dictionary of string sizes by their global index


class Protofield:
    """
    wrapper for the context of a google.protobuf.descriptor.FieldDescriptor
    instance variables:
    path : the path to the proto field using dot (".") notation starting with the root message
    field_desc : a google.protobuf.descriptor.FieldDescriptor of the proto field.
    giz : a global index of the field, used to apply string and repeat size multipliers
    size_product : a multiplier to apply against the field. Used for repeated primitives, repeated sub messages and their primitives, or strings.
    instance methods:
        get_fq_name :  returns a concatnation of the field path and it's name

    """

    def __init__(self, path: str, field_desc: FieldDescriptor, gix: int, size_product=1, ):
        self.field_path = path
        self.field_desc = field_desc
        self.field_gix = gix
        self.field_size_product = size_product

    def _guess_size(self, field: FieldDescriptor):
        fd = FieldDescriptor
        SizeDict = {
            fd.TYPE_DOUBLE: 64,
            fd.TYPE_FLOAT: 21,
            fd.TYPE_INT64: 64,
            fd.TYPE_UINT64: 64,
            fd.TYPE_INT32: 32,
            fd.TYPE_FIXED64: 64,
            fd.TYPE_FIXED32: 32,
            fd.TYPE_BOOL: 4,
            fd.TYPE_STRING: 4,
            fd.TYPE_GROUP: NotImplemented,
            fd.TYPE_MESSAGE: 0,
            fd.TYPE_BYTES: NotImplemented,
            fd.TYPE_UINT32: 32,
            fd.TYPE_ENUM: 8,
            fd.TYPE_SFIXED32: 32,
            fd.TYPE_SFIXED64: 64,
            fd.TYPE_SINT32: 43,
            fd.TYPE_SINT64: 64,
        }
        return SizeDict[field.type] * self.field_size_product

    def get_fq_name(self):
        return self.field_path + self.field_desc.name


class Protohelper:
    """

    """

    def __init__(self):
        self.string_size_index = {}
        self.repeat_size_index = {}

    def _find_msg_repeat_max(self, gix):
        self.string_size_index.get(gix, 1)

    def _find_str_size_max(self, gix):
        self.string_size_index.get(gix, 1)

    def fq_fields(self, message, _path=None, _gix=-1, _repeat_multiplier=1):
        """
        Recursively crawls through a message and sub message. Uses this class instance variables string_size_index and repeat_size_index to help size
        :param message: a google.protobuf.message.Message
        :param _path: used by the recusive call to track the location using dot (.) notation. For example
        :param _gix: Global index used to id where a message is within the stack.
        TODO replace this _gix with just a string since indexes are a bit more problimatic
        :param _repeat_multiplier: used by the recursive call
        :return: a generator of Protofields
        """
        # init the path when we enter with the message name.
        if not _path:
            _path = message.DESCRIPTOR.name + "."
        # handle messages (root) or message descriptors (from sub messages)
        if isinstance(message, type(Descriptor)):
            descriptor = message
        elif isinstance(message, Message):
            descriptor = message.DESCRIPTOR
        message_fields = descriptor.fields
        for field in message_fields:
            _gix += 1
            if field.type == FieldDescriptor.TYPE_MESSAGE:
                message_repeat_multplier = self._find_msg_repeat_max(_gix)
                yield Protofield(_path, field, _gix, message_repeat_multplier)
                yield from self.fq_fields(field.message_type,
                                          _path=_path + field.name + ".",
                                          _gix=_gix,
                                          _repeat_multiplier=message_repeat_multplier)
            if field.type == FieldDescriptor.TYPE_STRING:
                field_repeat_multiplier = self._find_str_size_max(_gix)
            else:
                yield Protofield(_path, field, _gix, _repeat_multiplier)


def _repeat_():
    pass


# basic test where we return the values and print them.
from app.protos import foo_pb2

msg = foo_pb2.SearchRequest()
ph = Protohelper()

for protofield in ph.fq_fields(msg):
    print(protofield.get_fq_name())
    # print(p, f.name, gi)

# more basic example where we gather the size
bits = 0
for p, f, _ in fq_fields(msg):
    try:
        bits += _guess_size(f)
    except:
        pass
print(f' I guess this is: {bits} bits long')

# structure for finding size.
# two part
# get the repeated field and return a query to find the max number of repeats.
# ie select max(t2.pos) from foo t1, t1.x t2 for a msg that is repeated
# ie select max(length(mystr) from foo for a str
# for submessages we need to return the sum of it's parts, this is where the _repeat_multiplier param comes in.
# as we traverse inward we will multiply any sub values. So an addresss book with multiple phone numbers will have the
# max phone numbers applied against the entire phone book.



msg.query = 'dsfsdf'
msg.page_number = 2
msg.result_per_page = 3

msg.sm.foo = '324324'
msg.sm.whatever = 323
w = msg.sm.w.add()
w.err = 'blahblahblah'
print(msg)

y = msg.DESCRIPTOR.fields[3]

# TODO extract all fields and produce the max size
# TODO extract all repeatable fields and generate a impala statement for getting max/avg
# TODO extract all string fields and generate a impala statement for getting max/avg
