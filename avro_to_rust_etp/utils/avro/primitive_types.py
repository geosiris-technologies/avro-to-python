""" file containing primitive types for avro """

PRIMITIVE_TYPES = {
    'null',
    'boolean',
    'int',
    'long',
    'float',
    'double',
    'bytes',
    'string'
}

PRIMITIVE_TYPE_MAP = {
    'null': 'None',
    'boolean': 'bool',
    'int': 'i32',
    'long': 'i64',
    'float': 'f32',
    'double': 'f64',
    # 'bytes': 'bytes::Bytes',
    'bytes': 'Vec<u8>',
    'string': 'String'
}
