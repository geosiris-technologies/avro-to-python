""" base Field class for avro field structure """

from typing import Union, List, Dict
from dataclasses import dataclass, field

@dataclass
class Field(object):

    name: str = None
    fieldtype: str = None
    default: Union[int, str, float, dict, None]=None

    def __eq__(self, other: Union['Field', str]):
        if isinstance(other, Field):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other

    def __str__(self):
        return f"Field(name={self.name}, fieldtype={self.fieldtype} "

    def __repr__(self):
        return f"<FieldObject:'{self.name}'>"
    

@dataclass
class ReferenceField(Field):
    reference_name: str = None
    reference_namespace: str = None

    def __str__(self):
        return "Reference"+super(ReferenceField, self).__str__() + f", reference_name={self.reference_name}, reference_namespace={self.reference_namespace} "

    def __repr__(self):
        return f"<ReferenceFieldObject:'{self.name}'>"

    def to_dict(self, already_added) -> Dict:
        return {}
        # if self.reference_name not in already_added:
            


@dataclass
class PrimitiveField(Field):
    avrotype: str = None

    def __str__(self):
        return "Primitive"+super(PrimitiveField, self).__str__() + f", avrotype={self.avrotype})"

    def __repr__(self):
        return f"<PrimitiveFieldObject:'{self.name}'>"

    def to_dict(self, already_added) -> Dict:
        return {}


@dataclass
class ArrayField(Field):
    array_item_type : Field = None

    def __str__(self):
        return "Array"+super(ArrayField, self).__str__() + f", array_item_type={self.array_item_type})"

    def __repr__(self):
        return f"<ArrayFieldObject:'{self.name}'>"

    def to_dict(self, already_added) -> Dict:
        return {"type": "array", "items": self.array_item_type}

@dataclass
class EnumField(Field):
    enum_type : Field = None

    def __str__(self):
        return "Enum"+super(EnumField, self).__str__() + f", enum_type={self.enum_type})"

    def __repr__(self):
        return f"<EnumFieldObject:'{self.name}'>"

    def to_dict(self, already_added) -> Dict:
        return { "type": "enum",
                    "name": self.enum_type.name,
                    "default": self.default
                    # "symbols" : self.symbols
                }

@dataclass
class MapField(Field):
    map_type: Field = None

    def __str__(self):
        return "Map"+super(MapField, self).__str__() + f", map_type={self.map_type})"

    def __repr__(self):
        return f"<MapFieldObject:'{self.name}'>"

    def to_dict(self, already_added) -> Dict:
        return {}

@dataclass
class UnionField(Field):
    union_types: List[Field] = field(default_factory=list)
    optional: bool = False

    def __str__(self):
        return "Union"+super(UnionField, self).__str__() + f", union_types={self.union_types})"

    def __repr__(self):
        return f"<UnionFieldObject:'{self.name}'>"

    def to_dict(self, already_added) -> Dict:
        return {}

# @dataclass
# class FixedField(Field):
