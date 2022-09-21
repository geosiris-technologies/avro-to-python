""" base file class for avro file structure """

from typing import List, Union, Mapping
from dataclasses import dataclass, field

from avro_to_python_etp.classes.field import Field
from avro_to_python_etp.classes.reference import Reference

@dataclass
class File(object):

    name: str = None
    avrotype: str = None
    namespace: str = None
    schema: dict = None
    expanded_schema: dict = None
    expanded_types: List[object] = field(default_factory=list)
    imports: List[Reference] = field(default_factory=list)
    fields: Mapping[str, Field] = field(default_factory=list)
    enum_sumbols: List[str] = field(default_factory=list)
    #meta_fields: List[object] = field(default_factory=list)

    def __eq__(self, other: Union['File', str]):
        if isinstance(other, File):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other

    def __repr__(self):
        return f"<FileObject:'{self.name}' - {self.imports}>"

    def expand(self):                
        # print(self.expanded_schema)
        self.expanded_schema['fields']=[]
        # print(self.expanded_schema)
        already_added = []
        # print(self.fields)
        for f in self.fields.values():            
            if f.name not in already_added:
                self.expanded_schema['fields'].append(f.to_dict(already_added))
                already_added.append(f.name)
        
        # print(self.expanded_schema)

    def has_uuid_field(self):
        for imp in self.imports:
            if imp.name == "Uuid":
                return True

        return False