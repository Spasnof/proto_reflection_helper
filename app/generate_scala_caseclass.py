from google.protobuf.descriptor import Descriptor, FieldDescriptor
import argparse
# refer to the entrypoint.sh on how this is generated.
import protos.entrypoint_pb2 as entrypoint_proto
import os

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

def TelemPBfield_to_ScalaLiteral(field: FieldDescriptor, LiteralInteger: int):
    '''
        Creates scala case class Literal based on proto class.
    '''
    fd = FieldDescriptor
    if field.type == fd.TYPE_MESSAGE:
        return f'Mock{field.message_type.name}'
    TypeDict = {
        fd.TYPE_DOUBLE: f'{LiteralInteger}',
        fd.TYPE_FLOAT: f'{LiteralInteger}f',
        fd.TYPE_INT64: f'{LiteralInteger}l',
        fd.TYPE_UINT64: f'{LiteralInteger}l',
        fd.TYPE_INT32: f'{LiteralInteger}',
        fd.TYPE_FIXED64: f'{LiteralInteger}l',
        fd.TYPE_FIXED32: f'{LiteralInteger}',
        fd.TYPE_BOOL: f'{LiteralInteger % 2 == 0}'.lower(),
        fd.TYPE_STRING: f'"{LiteralInteger}"',
        fd.TYPE_GROUP: NotImplemented,
        fd.TYPE_BYTES: NotImplemented,
        fd.TYPE_UINT32: f'{LiteralInteger}',
        fd.TYPE_ENUM: f'"ENUM-{LiteralInteger}"',
        fd.TYPE_SFIXED32: f'{LiteralInteger}',
        fd.TYPE_SFIXED64: f'{LiteralInteger}l',
        fd.TYPE_SINT32: f'{LiteralInteger}',
        fd.TYPE_SINT64: f'{LiteralInteger}l',
    }
    return TypeDict[field.type]

def create_mock_of_case_class(desc_obj: Descriptor, msg_name: str) -> str:
    '''
    Creates mock of case classes out of messages
    '''
    global GlobalIterable
    literalArray = []
    for field_name, DescriptorObj in desc_obj.fields_by_name.items():
        GlobalIterable += 1
        literalArray.append(f'{field_name} =  {TelemPBfield_to_ScalaLiteral(DescriptorObj, GlobalIterable)}')
    case_class_template = '''
    val Mock{classIdentifier} = {classIdentifier}(
    {literalArray}
    )
    '''
    return case_class_template.format(classIdentifier=msg_name, literalArray=',\n\t'.join(literalArray))


GlobalIterable = 0
if __name__ == '__main__':
    desc = entrypoint_proto.DESCRIPTOR
    # generate case classes
    case_classes = []
    for messageName, descObj in desc.message_types_by_name.items():
        case_classes.append(create_case_class(descObj, messageName))
    generate_class_mocks = []
    case_class_mocks = []
    # generate case class mock objects
    for messageName, descObj in desc.message_types_by_name.items():
        case_class_mocks.append(create_mock_of_case_class(descObj, messageName))

    # print our individual case classes
    for case_class in case_classes:
        print(case_class)

    # print a single trait with mock objects filled in based on case class
    TraitName = 'Mock' + os.environ['ENTRYPROTO'].replace('.proto', '')
    case_class_mocks_exploded = '\n\t'.join(case_class_mocks)
    trait_with_mocks = f'''trait {TraitName} {{
        {case_class_mocks_exploded}
}}'''
    print(trait_with_mocks)

    # add a scala main class just to finish it off.
    MockObjects = ['println(Mock' + messageName + ')\n' for messageName in desc.message_types_by_name]
    print_mocks_exploded = '\t\t'.join(MockObjects)
    main_class = f'''object PrintMocks extends {TraitName} {{
    def main(args: Array[String]):Unit = {{
        {print_mocks_exploded}
    }}
}}'''
    print(main_class)
