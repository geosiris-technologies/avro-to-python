""" base Reference class """

from typing import Union
from dataclasses import dataclass, field

@dataclass
class Reference(object):

    name: str
    namespace: str

    def __eq__(self, other: Union['Reference', str]):
        return self.name + self.namespace == other.name + other.namespace

    def __repr__(self):
        return f"<Reference:'{self.name}'>"
