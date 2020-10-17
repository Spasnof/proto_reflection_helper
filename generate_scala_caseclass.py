from google.protobuf.descriptor import Descriptor, FieldDescriptor
import foo_pb2

def create_case_class(desc_obj: Descriptor, msg_name: str) -> str:
    '''
    Creates case clases out of messages
    '''
    paramArray = []
    for field_name, DescriptorObj in desc_obj.fields_by_name.items():
        paramArray.append(f'{field_name}: {TelemPBfield_to_ScalaCCType(DescriptorObj)}')
    case_class_template = '''
case class {classIdentifier}(
{paramArray}
)
    '''
    return case_class_template.format(classIdentifier=msg_name, paramArray=',\n'.join(paramArray))

def TelemPBfield_to_ScalaCCType(field: FieldDescriptor):
    '''
        Creates scala case class type based on proto class.
    '''
    fd = FieldDescriptor
    if field.type == fd.TYPE_MESSAGE:
        return field.message_type.name
    TypeDict = {
        fd.TYPE_DOUBLE: 'Double',
        fd.TYPE_FLOAT: 'Float',
        fd.TYPE_INT64: 'Long',
        fd.TYPE_UINT64: 'Long',
        fd.TYPE_INT32: 'Int',
        fd.TYPE_FIXED64: 'Long',
        fd.TYPE_FIXED32: 'Int',
        fd.TYPE_BOOL: 'Bool',
        fd.TYPE_STRING: 'String',
        fd.TYPE_GROUP: NotImplemented,
        fd.TYPE_BYTES: NotImplemented,
        fd.TYPE_UINT32: 'Int',
        fd.TYPE_ENUM: 'String',
        fd.TYPE_SFIXED32: 'Int',
        fd.TYPE_SFIXED64: 'Long',
        fd.TYPE_SINT32: 'Int',
        fd.TYPE_SINT64: 'Long',
    }
    return TypeDict[field.type]


desc = foo_pb2.DESCRIPTOR
for messageName, descObj in desc.message_types_by_name.items():
    print(create_case_class(descObj, messageName))