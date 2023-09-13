""" Writer class for writing python avro files """
import os 
import re 

import json
import pkg_resources
import shutil
from typing import Any, List
from anytree import Node, LevelOrderIter
from textwrap import TextWrapper, fill, wrap
from jinja2 import Environment, FileSystemLoader

import keyword

from avro_to_rust_etp.utils.avro.helpers import get_union_types, split_words, get_union_types_enum_name
from avro_to_rust_etp.utils.avro.primitive_types import PRIMITIVE_TYPE_MAP
from avro_to_rust_etp.utils.paths import (
    get_system_path, verify_or_create_namespace_path, get_or_create_path,
    get_joined_path)


TEMPLATE_PATH = __file__.replace(get_joined_path('writer', 'writer.py'), 'templates/')
TEMPLATE_PATH = get_system_path(TEMPLATE_PATH)

RUST_RESEVED_KEYWORDS = [ "as", "use", "extern crate", "break", "const", "continue", "crate", "else", "if", "if let", "enum", "extern", "false", "fn", "for", "if", "impl", "in", "for", "let", "loop", "match", "mod", "move", "mut", "pub", "impl", "ref", "return", "Self", "self", "sel+f", "static", "struct", "super", "trait", "true", "type", "unsafe", "use", "where", "while", "abstract", "alignof", "become", "box", "do", "final", "macro", "offsetof", "override", "priv", "proc", "pure", "sizeof", "typeof", "unsized", "virtual", "yield"
]

RUST_FILE_LICENSE = """// SPDX-FileCopyrightText: 2023 Geosiris
// SPDX-License-Identifier: Apache-2.0 OR MIT
"""


def rgx_sub(pattern: str, repl: str, value: str) -> str:
    print("REGEX")
    print(pattern, repl, value)
    return re.sub(pattern, repl, str(value))

    
class AvroWriter(object):
    """ writer class for writing python files

    Should initiate around a tree object with nodes as:

    {
        'children': {},
        'files': {},
        'visited': False
    }

    The "keys" of the children are the namespace names along avro
    namespace paths. The Files are the actual files within the
    namespace that need to be compiled.

    Note: The visited flag in each node is only for node traversal.

    This results in the following behavior given this sample tree:

    tree = {
        'children': {'test': {
            'children': {},
            'files': {'NestedTest': ...},
            'visited': False
        }},
        'files': {'Test' ...},
        'visited': False
    }

    files generated:
    /Test.py
    /test/NestedTest.py
    """
    root_dir = None
    files = []

    def __init__(self, tree: Node, pip: str=None, author: str=None,
                 package_version: str=None) -> None:
        """ Parses tree structured dictionaries into python files

        Parameters
        ----------
            tree: dict
                tree object
                acyclic tree representing a read avro schema namespace
            pip: str
                pip package name
            author: str
                author of pip package

        Returns
        -------
            None

        TODO: Check tree is valid
        """
        self.pip = pip
        self.author = author
        self.package_version = package_version
        self.tree = tree

        # jinja2 templates
        self.template_env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
        self.template_env.filters.update({
            "pascal_case": self.pascal_case,
            "snake_case_module": self.snake_case_module,
            "snake_case": self.snake_case,
            "compress": self.compress,
            "screaming_snake_case": self.screaming_snake_case,
            "lower_and_snake": self.lower_and_snake,
            "lower_and_snake_module": self.lower_and_snake_module,
            "is_reserved": self.is_reserved
            })
        self.template = self.template_env.get_template('baseTemplate.j2')


        self.enum_types = []
        for node in LevelOrderIter(self.tree):
            for c in node.children:
                if c.is_leaf:
                    f = c.file
                    if f.schema is not None and f.schema['type'] == "enum":
                        self.enum_types.append(f.name)
        print(">$>", self.enum_types)



    def lower_and_snake(self, value: str, **kwargs: Any) -> str:
        split = value.split('.')
        return "%s" % '.'.join([self.snake_case(str(x)) for x in split])

    def lower_and_snake_module(self, value: str, **kwargs: Any) -> str:
        split = value.split('.')
        return "%s" % '.'.join([self.snake_case(str(x)) for x in split]).replace(".", "::")
        
    def snake_case(self, value: str, **kwargs: Any) -> str:
        """Convert the given string to snake case."""

        if not isinstance(value, str):
            value = str(value)

        return "_".join(map(str.lower, split_words(value)))
        
    def snake_case_module(self, value: str, **kwargs: Any) -> str:
        """Convert the given string to snake case."""
        return "_".join(map(str.lower, split_words(value))).replace(".", "::")

    def is_reserved(self, value: str, **kwargs: Any) -> bool:
        return value in RUST_RESEVED_KEYWORDS

    def pascal_case(self, value: str, **kwargs: Any) -> str:
        return "".join(map(lambda w : w[0].upper() + w[1:], value.split("_")))

    def compress(self, value: str, **kwargs:Any) -> str:
        """Compress and wraps the given string."""
        
        schema =""
        for line in wrap(value, width=70):
            # print("---------")
            # print("'{}'".format(line))
            schema += "'{}'".format(line)
            schema += "\n"
            # print("---------")
        # print(schema)
        return schema #fill(value, width=70)

    def screaming_snake_case(self, value: str, **kwargs: Any) -> str:
        """Convert the given string to screaming snake case."""
        return self.snake_case(value, **kwargs).upper()

    def write(self, root_dir: str) -> None:
        """ Public runner method for writing all files in a tree

        Parameters
        ----------
            root_path: str
                root path to write files to

        Returns
        -------
            None
        """

        self.root_dir = get_system_path(root_dir)
        if self.pip:
            self.pip_import = self.pip.replace('-', '_')
            self.pip_dir = self.root_dir + '/' + self.pip
            self.root_dir += '/' + self.pip + '/src'  # + self.pip.replace('-', '_')
            self.pip = self.pip.replace('-', '_')
        else:
            self.pip_import = ''
        get_or_create_path(self.root_dir)

        self._write_dfs()

        self._write_protocols_helper()
        # self._write_default_protocols_file()
        # self._write_helper_file()
        # self._write_lib_file()
        # self._write_error_file()
        # self._write_message_file()
        # self._write_message_impl_file()
        
        if self.pip:
            self._write_cargo_file()

        self.copy_raw()
        self.gen_mods_files()
        # self.copy_tests()

    def copy_raw(self):
        test_dir = self.pip_dir
        folder = pkg_resources.resource_filename("avro_to_rust_etp", "raw_files")
        for path, dirs, files in os.walk(folder):
            cur_folder = path.replace(folder, "")
            while cur_folder.startswith("/") or cur_folder.startswith("\\"):
                cur_folder = cur_folder[1:]

            cur_folder = self.pip_dir + "/" + cur_folder

            try:
                os.makedirs(cur_folder)
            except FileExistsError:
                pass
            for file_name in files:
                shutil.copy(path + "/" + file_name, cur_folder + "/" + file_name)


    def gen_mods_files(self):

        for path, dirs, files in os.walk(self.root_dir):
            # print(f"DIRS : {dirs} -- {path} __ {files}\n")
            if not path.endswith("/src"):
                if len(dirs) > 0 or len(files) > 0:
                    self._write_mod_file(file_path = path + ".rs",
                                         sub_modules = list(dict.fromkeys(dirs + list(map(lambda x: x.replace(".rs", "") , list(filter(lambda x: x.endswith(".rs"), files)) )) ))
                                        )


    def _write_message_impl_file(self) -> None:
        """ writes the message_impl.rs file to the pip dir"""
        filepath = self.pip_dir + '/src/message_impl.rs'
        template = self.template_env.get_template('files/message_impl.j2')
        filetext = template.render(
            pip=self.pip,
            author=self.author,
            package_version=self.package_version
        )
        with open(filepath, 'w') as f:
            f.write(RUST_FILE_LICENSE)
            f.write(filetext)

    def _write_cargo_file(self) -> None:
        """ writes the cargo.toml file to the pip dir"""
        filepath = self.pip_dir + '/Cargo.toml'
        template = self.template_env.get_template('files/cargo.j2')
        filetext = template.render(
            pip=self.pip,
            author=self.author,
            package_version=self.package_version
        )
        with open(filepath, 'w') as f:
            f.write(filetext)

    def _write_default_protocols_file(self) -> None:
        """ writes the default_protocol.rs file to the root dir """
        filepath = self.pip_dir + '/src/default_protocols.rs'
        template = self.template_env.get_template('files/default_protocols.j2')

        # Search protocol :
        protocols = []
        all_types = []
        for node in LevelOrderIter(self.tree, filter_=lambda n: not n.is_leaf):
            imports = set()
            path = [str(n.name) for n in node.path]
            namespace = "%s" % '.'.join([self.snake_case(str(x)) for x in path])
            
            for c in node.children:
                if c.is_leaf:
                    f = c.file
                    if f.schema is not None:
                        all_types.append(f)
                    if "protocol" in f.schema:
                        print("P)\t", f)
                        protocols.append(f)

        protocols.sort(key=lambda r : (int(r.schema["protocol"]), int(r.schema["messageType"])))

        filetext = template.render(
            protocols=protocols,
            all_types=list(set(map(lambda x : json.dumps(x.schema), all_types))),
            primitive_type_map=PRIMITIVE_TYPE_MAP,
            get_union_types=get_union_types,
            get_union_types_enum_name=get_union_types_enum_name,
            pascal_case=lambda w: self.pascal_case(w),
            rgx_sub=rgx_sub,
            json=json,
            pip_import=self.pip_import,
            enumerate=enumerate,
        )
        with open(filepath, 'w') as f:
            f.write(RUST_FILE_LICENSE)
            f.write(filetext)

    def _write_protocols_helper(self) -> None:
        """ writes the default_protocol.rs file to the root dir """
        filepath = self.pip_dir + '/src/protocols.rs'
        template = self.template_env.get_template('files/protocol_helper.j2')

        # Search protocol :
        protocols = []
        all_types = []
        for node in LevelOrderIter(self.tree, filter_=lambda n: not n.is_leaf):
            imports = set()
            path = [str(n.name) for n in node.path]
            namespace = "%s" % '.'.join([self.snake_case(str(x)) for x in path])
            
            for c in node.children:
                if c.is_leaf:
                    f = c.file
                    if f.schema is not None:
                        all_types.append(f)
                    if "protocol" in f.schema:
                        print(f)
                        protocols.append(f)

        protocols.sort(key=lambda r : (int(r.schema["protocol"]), int(r.schema["messageType"])))

        filetext = template.render(
            protocols=protocols,
            all_types=list(set(map(lambda x : json.dumps(x.schema), all_types))),
            primitive_type_map=PRIMITIVE_TYPE_MAP,
            get_union_types=get_union_types,
            get_union_types_enum_name=get_union_types_enum_name,
            pascal_case=lambda w: self.pascal_case(w),
            rgx_sub=rgx_sub,
            json=json,
            pip_import=self.pip_import,
            enumerate=enumerate,
        )
        with open(filepath, 'w') as f:
            f.write(RUST_FILE_LICENSE)
            f.write(filetext)

    def _write_mod_file(self, sub_modules: list, file_path) -> None:
        """ writes __init__.py files for namespace imports"""
        template = self.template_env.get_template('files/mod.j2')
        filetext = template.render(
            sub_modules=sub_modules,
        )
        with open(file_path, 'w') as f:
            f.write(RUST_FILE_LICENSE)
            f.write(filetext)

    def _write_file(
        self, filename: str, filetext: str, namespace: str
    ) -> None:
        """ writes python filetext to appropriate namespace
        """
        verify_or_create_namespace_path(
            rootdir=self.root_dir,
            namespace=namespace
        )
        filepath = self.root_dir + '/' + namespace.replace('.', '/') + '/' + self.snake_case(filename) + '.rs'  # NOQA
        with open(filepath, 'w') as f:
            f.write(RUST_FILE_LICENSE)
            f.write(filetext)

    def _render_file(self, file: dict) -> str:
        """ compiles a file obj into python

        Parameters
        ----------
            file: dict
                file obj representing an avro file

        Returns
        -------
            filetext: str
                rendered python file as a sting
        """
        filetext = self.template.render(
            file=file,
            primitive_type_map=PRIMITIVE_TYPE_MAP,
            get_union_types=get_union_types,
            get_union_types_enum_name=get_union_types_enum_name,
            pascal_case=lambda w: self.pascal_case(w),
            json=json,
            enum_types=self.enum_types,
            pip_import=self.pip_import,
            enumerate=enumerate
        )
        return filetext

    def _write_dfs(self) -> None:

        for node in LevelOrderIter(self.tree, filter_=lambda n: not n.is_leaf):
            imports = set()
            path = [str(n.name) for n in node.path]
            namespace = "%s" % '.'.join([self.snake_case(str(x)) for x in path])
            
            for c in node.children:
                if c.is_leaf:
                    filetext = self._render_file(file=c.file)
                    self._write_file(
                        filename=c.file.name,
                        filetext=filetext,
                        namespace=namespace
                    )
                    imports.add(
                        c.file.name
                    )

    #    ____        __                      __
    #   / __ \__  __/ /_   ____  ____ ______/ /_
    #  / / / / / / / __/  / __ \/ __ `/ ___/ __/
    # / /_/ / /_/ / /_   / /_/ / /_/ / /  / /_
    # \____/\__,_/\__/  / .___/\__,_/_/   \__/
    #                  /_/ 

    def write_out(self, root_dir: str) -> None:
        self.root_dir = get_system_path(root_dir)
        if self.pip:
            self.pip_import = self.pip.replace('-', '_')
            self.pip_dir = self.root_dir + '/' + self.pip
            self.root_dir += '/' + self.pip + '/src'  # + self.pip.replace('-', '_')
            self.pip = self.pip.replace('-', '_')
        else:
            self.pip_import = ''

        get_or_create_path(self.root_dir)

        self.out_handler()

    def out_handler(self,):
        filepath = self.pip_dir + '/handlers.rs'
        template = self.template_env.get_template('out/handlers.j2')

        # Search protocol :
        protocols = []
        all_types = []
        for node in LevelOrderIter(self.tree, filter_=lambda n: not n.is_leaf):
            imports = set()
            path = [str(n.name) for n in node.path]
            namespace = "%s" % '.'.join([self.snake_case(str(x)) for x in path])
            
            for c in node.children:
                if c.is_leaf:
                    f = c.file
                    if f.schema is not None:
                        all_types.append(f)
                    if "protocol" in f.schema:
                        print(f)
                        protocols.append(f)

        protocols.sort(key=lambda r : (int(r.schema["protocol"]), int(r.schema["messageType"])))
        protocols_map = groupby(protocols, lambda r : int(r.schema["protocol"]))

        print(protocols_map)

        filetext = template.render(
            protocols=protocols_map,
            all_types=list(set(map(lambda x : json.dumps(x.schema), all_types))),
            primitive_type_map=PRIMITIVE_TYPE_MAP,
            get_union_types=get_union_types,
            get_union_types_enum_name=get_union_types_enum_name,
            pascal_case=lambda w: self.pascal_case(w),
            rgx_sub=rgx_sub,
            json=json,
            pip_import=self.pip_import,
            enumerate=enumerate,
        )
        with open(filepath, 'w') as f:
            f.write(RUST_FILE_LICENSE)
            f.write(filetext)


def groupby(lst: list, f):
    res = {}

    for v in lst:
        k = f(v)
        if k not in res:
            res[k] = []
        res[k].append(v)

    return res

# DONE : faire un trait pour les messages "protocol": "0", "messageType": "2", "senderRole": "server", "protocolRoles": "client, server", "multipartFlag"
# DONE : pub static AVRO_SCHEMA: &'static str = 
# TODO : ajouter les serialization / deserial avro ? ==> peut etre plutot dans etpproto  ?
# TODO : générer un match pour les couple protocol et message header ==> pour déserialiser les message en fonction du messsageHeader.
# TODO : voir si on supprime les chunck pour faire une seule struct (aussi modifier lors des imports : soit on vire les fichier chunck soit on laisse mais en pub use le manual chunck)
#           ==> voir si ils ont pas fait dejà la correction poru les protocol exception qui est un message dont le header peut avoir des "protocol" et "messageType" variable selon le message en erreur
# Regarder pour etpproto si on peut générer une lib avec option (comme python : pip install numpy[monoption]) ==> pour mettre dans la websocket en option pour réduire le code du client.

# TODO : voir si le dependabot peut voir depuis etptypes que avro-to-etp a une nouvelle version : crée une nouvelle branche et push le code. La main de etptypes aurait que le avpr.
# TODO :  incrémenter etptype  le numero de version autoamtuiquement a la CI mais en gardant le +1.2 apres le numero