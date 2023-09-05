""" contains helper function for parsing avro schema """

from typing import List, Tuple

from avro_to_rust_etp.classes.reference import Reference
from avro_to_rust_etp.classes.field import Field

from avro_to_rust_etp.utils.exceptions import BadReferenceError
from avro_to_rust_etp.utils.avro.primitive_types import PRIMITIVE_TYPE_MAP
import re

def _create_reference(file: dict) -> dict:
    """ creates a reference object for file references

    Parameters
    ----------
        file: dict
            object containing information on a complex avro type to reference

    Returns
    -------
        reference: dict
            object containing reference information
    """
    if any([('name' not in file), ('namespace') not in file]):
        raise BadReferenceError

    return Reference(
        name=file['name'],
        namespace=file['namespace']
    )


def _get_namespace(obj: dict, parent_namespace: str=None) -> None:
    """ imputes the namespace if it doesn't already exist

    Namespaces follow the following chain of logic:
        - Use a namespace if it exists
        - If no namespace is given:
            - If referenced in a schema, inherit the same namespace as  parent
            - if not referenced in a schema and no parent, namespace = ''
              resembling the root of the input dir.


    Parameters
    ----------
        obj: dict
            serialized object resembling an avsc schema
        parent_namespace: str
            parent object namespace if applicable

    Returns
    -------
        None
    """
    if obj.get('namespace', None):
        return obj['namespace']
    elif parent_namespace:
        return parent_namespace
    else:
        return ''

def pascal_case(value: str) -> str:
    return "".join(map(lambda w : w[0].upper() + w[1:], value.split("_")))

def get_union_types_enum_name(union_types: str):
    union_array = list(union_types.split(','));
    if len(union_array) == 1:
        return PRIMITIVE_TYPE_MAP.get(union_array[0], union_array[0])
    elif len(union_array) == 2 and (union_array[0].lower() == "null" or union_array[1].lower() == "null"):
        if union_array[0].lower() == "null":
            return PRIMITIVE_TYPE_MAP.get(union_array[1], union_array[1])
        else:
            return PRIMITIVE_TYPE_MAP.get(union_array[0], union_array[0])
    else:
        return "Union" + ''.join(map(pascal_case, union_array))

def get_type(obj, primitive_type_map: dict=PRIMITIVE_TYPE_MAP):
    # primitive type
    if obj.fieldtype == 'primitive':
        if primitive_type_map is not None:
            return primitive_type_map.get(obj.avrotype)
        else:
            return obj.avrotype
    # reference to a named type
    elif obj.fieldtype == 'reference':
        return obj.reference_name

    elif obj.fieldtype == 'array':
        return 'list'
    else:
        raise ValueError('unsupported type')

def get_union_types(
    field: Field,
    use_strict: bool = True,
    primitive_type_map: dict=PRIMITIVE_TYPE_MAP
) -> str:
    """ Takes a field object and returns the types of the fields

    Parameters
    ----------
        field: dict
            dictionary resembling a field for a union type
        PRIMITIVE_TYPE_MAP: dict
            lookup table mapping avro types to python types

    Returns
    -------
        out_types: str
            comma seperated string of python types
    """

    out_types = []

    for obj in field.union_types:
        out_types.append(get_type(obj, primitive_type_map))
        # # primitive type
        # if obj.fieldtype == 'primitive':
        #     if PRIMITIVE_TYPE_MAP is not None:
        #         out_types.append(PRIMITIVE_TYPE_MAP.get(obj.avrotype))
        #     else:
        #         out_types.append(obj.avrotype)


        # # reference to a named type
        # elif obj.fieldtype == 'reference':
        #     out_types.append(obj.reference_name)

        # elif obj.fieldtype == 'array':
        #     out_types.append('list')

        # else:
        #     raise ValueError('unsupported type')

    return ','.join(out_types)


def dedupe_imports(imports: List[Reference]) -> None:
    """ Dedupes list of imports

    Parameters
    ----------
        imports: list of dict
            list of imports of a file

    Returns
    -------
        None
    """
    hashmap = {}
    for i, obj in enumerate(imports):
        hashmap[obj.name + obj.namespace] = obj

    return list(hashmap.values())


def split_namespace(s: str) -> Tuple[str, str]:
    """ Splits a namespace and name into their parts

    Parameters
    ----------
        s: str
            string to be split

    Returns
    -------
        (tuple)
            namespace: str
            name: str
    """
    split = s.split('.')
    name = split.pop()
    namespace = '.'.join(split)
    return (namespace, name)

class StringType:
    UPPER = 1
    LOWER = 2
    NUMERIC = 3
    OTHER = 4
    
def classify(character: str) -> int:
    """String classifier."""
    if character.isupper():
        return StringType.UPPER
    if character.islower():
        return StringType.LOWER
    if character.isnumeric():
        return StringType.NUMERIC

    return StringType.OTHER

def split_words(value: str) -> List[str]:
    """Split a string on new capital letters and not alphanumeric
    characters."""
    words: List[str] = []
    buffer: List[str] = []
    previous = None

    def flush():
        if buffer:
            words.append("".join(buffer))
            buffer.clear()

    for char in value:
        tp = classify(char)
        if tp == StringType.OTHER:
            flush()
        elif not previous or tp == previous:
            buffer.append(char)
        elif tp == StringType.UPPER and previous != StringType.UPPER:
            flush()
            buffer.append(char)
        else:
            buffer.append(char)

        previous = tp

    flush()
    return words    

def safe_snake(string: str, default: str = "value") -> str:
    """
    Normalize the given string to make it safe for python source code.

    Return or prepend the default value if after all filters the result
    is invalid.
    """
    if not string:
        return default

    if not isinstance(string, str):
        string = str(string)

    if re.match(r"^-\d*\.?\d+$", string):
        return f"{default}_minus_{string}"

    # Remove invalid characters
    string = re.sub("[^0-9a-zA-Z_-]", " ", string).strip()

    if not string:
        return default

    string = string.strip("_")

    if not string[0].isalpha():
        return f"{default}_{string}"

    if string.lower() in stop_words:
        return f"{string}_{default}"

    return string