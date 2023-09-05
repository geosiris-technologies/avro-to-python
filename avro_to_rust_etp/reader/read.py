""" contains class and methods for reading avro files and dirs """

import copy
import os
import json
from typing import Any, List

from anytree import Node, RenderTree, PostOrderIter, search
from nested_lookup import nested_lookup, nested_update

# from avro_to_rust_etp.classes.node import Node
from avro_to_rust_etp.classes.file import File

from avro_to_rust_etp.utils.paths import (
    get_system_path, get_avsc_files, verify_path_exists
)
from avro_to_rust_etp.utils.exceptions import (
    NoFileOrDir, MissingFileError, NoFilesError
)

from avro_to_rust_etp.utils.avro.helpers import _get_namespace, split_namespace, split_words
from avro_to_rust_etp.utils.avro.files.enum import _enum_file
from avro_to_rust_etp.utils.avro.files.record import _record_file
from avro_to_rust_etp.utils.avro.files.fixed import _fixed_file
from avro_to_rust_etp.utils.avro.primitive_types import PRIMITIVE_TYPES
from avro_to_rust_etp.utils.avro.types.type_factory import _get_field_type

# from avro_to_rust_etp.utils.avro.files.meta import _meta_file

import json

class AvscReader(object):
    """
    reader object for avro avsc files

    Should contain all logic for reading and formatting information
    within a dir of avsc files or a single file
    """
    file_tree = None

    def __init__(self, directory: str=None, file: str=None) -> None:
        """ Initializer should just create a list of files to process

        Parameters
        ----------
            directory: str
                Directory of files to read
                Cannot be used with "file" param

            file: str
                path of avsc file to compile
                Cannot be used with "directory" param

        Returns
        -------
            None
        """

        # initialize cental object
        self.obj = {}
        self.file_tree = None

        if directory:
            if os.path.isfile(directory):
                raise OSError(f'{directory} is a file!')
            files = get_avsc_files(directory)
            if files:
                self.files = files
                self.obj['root_dir'] = get_system_path(directory)
                self.obj['read_type'] = 'directory'
            else:
                raise NoFilesError(f'No avsc files found in {directory}')

        elif file:
            if not verify_path_exists(file):
                raise MissingFileError(f'{file} does not exist!')
            if os.path.isdir(file):
                raise IsADirectoryError(f'{file} is a directory!')
            syspath = get_system_path(file)
            self.files = [syspath]
            self.obj['read_type'] = 'file'

        else:
            raise NoFileOrDir

        self.obj['avsc'] = []


    def snake_case(self, value: str, **kwargs: Any) -> str:
        """Convert the given string to snake case."""
        return "_".join(map(str.lower, split_words(value)))
        
    def read(self):
        """ runner method for AvscReader object """
        self._read_files()        
        self._build_namespace_tree()
        self._expand_schemas()

    def _read_files(self) -> None:
        """ reads and serializes avsc files to central object
        """
        for file in self.files:
            with open(file, 'r') as f:
                serialized = json.load(f)
                self.obj['avsc'].append(serialized)

    def _build_namespace_tree(self) -> None:
        """ builds tree structure on namespace
        """
        # populate queue prior to tree building
        queue = copy.deepcopy(self.obj['avsc'])

        nodes = {}

        while queue:
            # get first item in queue
            item = queue.pop(0)

            save_schema = copy.deepcopy(item)            

            # impute namespace
            item['namespace'] = _get_namespace(item)            

            # traverse to namespace starting from root_node                 
            namespaces = item['namespace'].split('.')
            

            current_node = None
            for name in namespaces:
                if name not in nodes:                    
                    nodes[name] = Node(name=name, parent=current_node)                
                
                current_node = nodes[name]

            print(f"Reading {item['name']}")

            # initialize empty file obj for mutation
            file = File(
                name=item['name'],
                avrotype=item['type'],
                namespace=item['namespace'],
                schema=save_schema,
                expanded_schema=save_schema,
                expanded_types=[],
                fields={},
                imports=[],
                enum_sumbols=[]
            )

            # keys = [x for x in item.keys() if x not in ['name','type','namespace','fields']]
            # _meta_file(file, item, keys)
            
            # handle record type
            if file.avrotype == 'record':
                _record_file(file, item, queue)
            # handle enum type file
            elif file.avrotype == 'enum':
                _enum_file(file, item)
            # handle fixed type file
            elif file.avrotype == 'fixed':
                _fixed_file(file, item)
            else:
                raise ValueError(f"{item['type']} is currently not supported.")
            

            Node(name=item['name'], parent=current_node, file=file) 

        self.file_tree = next(iter(nodes.values())).root


    def _reshape_type2(self, typescheme, exclusionTypes, isroot, map_all_types):

        dependTable = typescheme["depends"]

        typescheme["depends"] = []
        # namespace = typescheme["namespace"]
        # if not isroot:
        #     typescheme.pop("namespace", None)

        string_view = json.dumps(typescheme)

        for dependTypeName in dependTable:
            if dependTypeName not in exclusionTypes:
                depend_obj, exclusionTypes = self._reshape_type2(map_all_types[dependTypeName], exclusionTypes, False, map_all_types)
                string_view = string_view.replace('"'+dependTypeName+'"', json.dumps(depend_obj), 1)
                exclusionTypes.append(dependTypeName)

        val = json.loads(string_view)
        # if isroot:
        val["depends"] = dependTable
        #else:
        #    val.pop("depends", None)
        typescheme["depends"] = dependTable
        # if not isroot:
        #     typescheme["namespace"] = namespace
        return (val, exclusionTypes)



    def _loop_reshape2(self, map_all_types):
        mapRes = {}
        for schemeName in map_all_types:
            mapRes[schemeName] = self._reshape_type2(map_all_types[schemeName], [], True, map_all_types)        
        return mapRes


    def _expand_schemas(self) -> None:

        all_schemas = []
        
        # finit = open("./init_avsc.avpr", "w")
        # finit.write(json.dumps(self.obj['avsc'], indent=2))
        # finit.close()

        # 1 step: do all depends
        for node in self.file_tree.leaves: 
            depends_list = [ref.namespace+'.'+ref.name for ref in node.file.imports]                
            node.file.expanded_schema['depends'] = depends_list
            all_schemas.append(node.file.expanded_schema)  
            # print("------------------------")
            # print(json.dumps(node.file.schema, indent=1))
            # print(json.dumps(node.file.expanded_schema, indent=1))
            # print("------------------------")
                 
        # finit = open("./inter_avsc.avpr", "w")
        # finit.write(json.dumps(all_schemas, indent=2))
        # finit.close()

        
        map_not_finished_type = {}

        for current_type in all_schemas:
            map_not_finished_type[current_type["namespace"] + "." + current_type["name"]] = current_type

        # print(map_not_finished_type)
        temp = self._loop_reshape2(map_not_finished_type)        
        self.obj['expanded_avsc'] = list(temp.values())

        for node in self.file_tree.leaves:
            f = temp[node.file.namespace+"."+node.file.name]        
            node.file.expanded_schema = f[0]


        # print("-----------------")
        # print(json.dumps(self.obj['expanded_avsc'], indent=4))
        # fres = open("./res_avsc.avpr", "w")
        # fres.write(json.dumps(self.obj['expanded_avsc'], indent=2))
        # fres.close()
          
