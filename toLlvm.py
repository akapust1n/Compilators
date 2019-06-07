from pycparser import c_parser, c_ast
import copy
import sys
import contextlib
from llvmlite import ir
from llvmlite.ir import NamedValue
from typing import Union

type_to_llvm_type = {'int': ir.IntType(64),
                     'char': ir.IntType(64)  # Not accurate/optimal. Whatever.
                     }


class CustomBuilder(ir.IRBuilder):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @contextlib.contextmanager
    def _branch_helper_goto_start(self, bbenter, bbexit, add_terminal=True):
        """
        :param add_terminal: If False do not add a terminal to the bbenter block, even if the user did not provide one.
        I'm using it to be able to set a custom terminal after this context manager has been used.
        :return:
        """
        self.position_at_start(bbenter)
        yield bbexit
        if add_terminal:
            if self.basic_block.terminator is None:
                self.branch(bbexit)


class LlvmConverterState:

    def __init__(self):
        self.functions = {}  # A map function name => llvmlite function object
        self.arg_identifiers_to_index = {}
        # TODO: add identifier_to_llvm_value for vars. Make arg_identifiers... consistent with it!
        # We should even have only ONE way of handling functions, args variables and variables.
        # Mb some kind of scope concerns later on though.
        # We dont have the args variables when we're just writing the function declaration though
        self.identifier_to_var = {}


llvm_converter_state = LlvmConverterState()


builder = CustomBuilder()


def getType(decl):
    """ Recursively explains a type decl node
    """
    typ = type(decl)

    if typ == c_ast.TypeDecl:
        quals = ' '.join(decl.quals) + ' ' if decl.quals else ''
        return quals + getType(decl.type)
    elif typ == c_ast.Typename or typ == c_ast.Decl:
        return getType(decl.type)
    elif typ == c_ast.IdentifierType:
        return ' '.join(decl.names)
    elif typ == c_ast.PtrDecl:
        quals = ' '.join(decl.quals) + ' ' if decl.quals else ''
        return quals + 'pointer to ' + getType(decl.type)
    elif typ == c_ast.ArrayDecl:
        arr = 'array'
        if decl.dim:
            arr += '[%s]' % decl.dim.value

        return arr + " of " + getType(decl.type)

    elif typ == c_ast.FuncDecl:
        if decl.args:
            params = [_explain_type(param) for param in decl.args.params]
            args = ', '.join(params)
        else:
            args = ''

        return ('function(%s) returning ' % (args) +
                getType(decl.type))


def _explain_type(node, module: Union[ir.Module, None] = None):
    """ Recursively explains a type decl node
    """
    if(len(node.attr_names) == 0):
        print("hot")
        for (child_name, child) in node.children():

            _explain_type(child, module)
   # typ = type(node)
    # print('start')
    # print(typ)
    print(type(node))
    if(isinstance(node, c_ast.Decl)):
        print('finde decl!')
        print(node.name)
        # print(getType(node))
        variable = builder.alloca(ir.IntType(64), name=node.name)
       # llvm_converter_state.identifier_to_var[node.name] = variable
        return variable
       # print(node)
    if(isinstance(node, c_ast.IdentifierType)):
        print(node.names)
        print("dfdsgsdg***********")
    if isinstance(node, c_ast.FileAST):
        module = ir.Module('generated', )
        # I got the triple from compiling a C program on my machine.
        module.triple = "x86_64-unknown-linux-gnu"
       # for statement in node.children:
       #     to_llvm(statement, builder, module=module)
     #   return module
        print(module)
        for (child_name, child) in node.children():

            _explain_type(child, module)
        return module
   # if(typ == c_ast.IdentifierType):
       # print('hello!')
