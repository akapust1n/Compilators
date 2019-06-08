import contextlib
from typing import Union

from llvmlite import ir
from llvmlite.ir import NamedValue

from tree import Function, Return, Integer, AstNode, BodyBlock, FunctionArgs, FunctionCall, \
    FunctionCallArgs, Declaration, Assignment, Char, BinOp, UnOp, Wrap, String, Identifier, If, ForLoop

dictr = {}


class CustomBuilder(ir.IRBuilder):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @contextlib.contextmanager
    def _branch_helper_goto_start(self, bbenter, bbexit, add_terminal=True):
        self.position_at_start(bbenter)
        yield bbexit
        if add_terminal:
            if self.basic_block.terminator is None:
                self.branch(bbexit)

    @contextlib.contextmanager
    def for_loop(self, condition_varname: str):
        bb = self.basic_block
        bbcond = self.append_basic_block(name=bb.name + '.forcondition')
        bbincr = self.append_basic_block(name=bb.name + '.forincrement')
        bbbody = self.append_basic_block(name=bb.name + '.for')
        bbend = self.append_basic_block(name=bb.name + '.endfor')

        self.branch(bbcond)

        self.position_at_end(bbincr)
        self.branch(bbcond)

        self.position_at_end(bbbody)
        self.branch(bbincr)

        for_cond = self._branch_helper_goto_start(
            bbcond, bbend, add_terminal=False)
        for_incr = self._branch_helper_goto_start(bbincr, bbend)
        for_body = self._branch_helper_goto_start(bbbody, bbend)
        yield for_cond, for_incr, for_body

        self.position_at_end(bbcond)
        condition_value = NamedValue(bbcond, ir.IntType(1), condition_varname)
        condition_value._name = condition_varname
        self.cbranch(condition_value, bbbody, bbend)

        self.position_at_end(bbend)


class LlvmConverterState:

    def __init__(self):
        self.functions = {}  # A map function name => llvmlite function object
        self.arg_identifiers_to_index = {}
        self.identifier_to_var = {}


llvm_converter_state = LlvmConverterState()


def function_to_llvm(node: Function, module: ir.Module):
    assert module is not None

    args = to_llvm(node.args, None,
                   module) if node.args is not None else tuple([])
    f_type = ir.FunctionType(ir.IntType(64), args)

    f = ir.Function(module, f_type, node.name.name)
    llvm_converter_state.functions[node.name.name] = f
    block = f.append_basic_block(name='entry')
    builder = CustomBuilder(block)
    to_llvm(node.body, builder, module)

    if not builder.block.instructions:
        builder.unreachable()
    return module


def return_to_llvm(node: Return, builder: CustomBuilder):
    """This function modifies builder inplace. It's a bit weird as it's not super consistent with other converters."""
    return builder.ret(to_llvm(node.value, builder))


def string_to_llvm(node):
    # TODO:
    pass


def char_to_llvm(node, builder, module):
    return to_llvm(Integer(ord(node.value)), builder, module)


def type_to_llvm_type(type):
    if(type == 'int' or type == 'char'):
        return ir.IntType(64)
    # )))))))))) это ужасно
    size = int(type.split("(")[1].split("name=")[1].split(")")[0])
    return ir.ArrayType(ir.IntType(64), size)


# type_to_llvm_type = {'int': ir.IntType(64),
 #                    'char': ir.IntType(64)
  #                   }


def to_llvm(node: AstNode, builder: Union[CustomBuilder, None] = None, module: Union[ir.Module, None] = None):
    if isinstance(node, Function):
        return function_to_llvm(node, module)
    if isinstance(node, BodyBlock):
        for statement in node.statements:
            to_llvm(statement, builder, module)
    if isinstance(node, FunctionArgs):
        arg_list = []
        for i, arg in enumerate(node.args):
            llvm_converter_state.arg_identifiers_to_index[arg.identifier.name] = i
            arg_list.append(type_to_llvm_type(arg.type))
        return tuple(arg_list)
    if isinstance(node, FunctionCall):
        args = [] if not node.args else to_llvm(node.args, builder, module)
        return builder.call(llvm_converter_state.functions[node.function_id.name], args)
    if isinstance(node, FunctionCallArgs):
        arg_list = []
        for arg in node.args:
            arg_list.append(to_llvm(arg, builder, module))
        return arg_list
    if isinstance(node, Declaration):
        # print(node.type)
        variable = builder.alloca(
            type_to_llvm_type(node.type), name=node.identifier.name)
        tmp = str(variable)
        index1 = tmp.find("[")+1
        if index1 > 0:
            index2 = tmp.find("]")
            count = int(tmp[index1: index2])
            new_type = node.type
            index = node.identifier.name.find("[")
            for i in range(0, count):
                new_name = node.identifier.name[:index]+"["+str(i)+"]"
                new_variable = builder.alloca(
                    type_to_llvm_type(new_type), name=new_name)
                llvm_converter_state.identifier_to_var[new_name] = new_variable
        else:
            llvm_converter_state.identifier_to_var[node.identifier.name] = variable
        if node.value is not None:
            if hasattr(node.value, "operation"):
                left = node.value.left
                if hasattr(left, "name"):
                    left = dictr[left.name]
                else:
                    left = left.value
                right = node.value.right
                if hasattr(right, "name"):
                    right = dictr[right.name]
                else:
                    right = right.value
                if node.value.operation == "+":
                    dictr[node.identifier.name] = right + left
                else:
                    dictr[node.identifier.name] = left - right
            return builder.store(to_llvm(node.value, builder, module), variable)
        else:
            return variable

    if isinstance(node, Assignment):
        """tmp = ""
        if node.identifier.name.find("[") > -1:
            index = node.identifier.name.index("[")
            numb = node.identifier.name[index+1]
            tmp = node.identifier.name[:index]
            ttmp = tmp + "[" + str(numb) + "]"
            llvm_converter_state.identifier_to_var[ttmp] = llvm_converter_state.identifier_to_var[tmp]
            llvm_converter_state.identifier_to_var[ttmp].type = i;
        for varr in llvm_converter_state.identifier_to_var:
            if varr.find("[") > -1:
                pass
                #llvm_converter_state.identifier_to_var"""
        if (node.identifier.name.find("[") > 0):
            index1 = node.identifier.name.find("[")+1
            index2 = node.identifier.name.find("]")
            varr = node.identifier.name[index1: index2]
            try:
                varr = int(varr)
            except:
                var1 = llvm_converter_state.identifier_to_var[str(
                    node.identifier.name).replace(varr, str(dictr[varr]))]
                return builder.store(to_llvm(node.value, builder, module), var1)
        elif hasattr(node.value, "value"):
            dictr[node.identifier.name] = node.value.value
        return builder.store(to_llvm(node.value, builder, module),
                             llvm_converter_state.identifier_to_var[node.identifier.name])
    if isinstance(node, Integer):
        return integer_to_llvm(node)
    if isinstance(node, Return):
        return return_to_llvm(node, builder)
    if isinstance(node, Char):
        return char_to_llvm(node, builder, module)
    if isinstance(node, BinOp):
        left = to_llvm(node.left, builder, module)
        right = to_llvm(node.right, builder, module)

        operation_to_method = {
            BinOp.ADD: builder.add,
            BinOp.SUBSTRACT: builder.sub,
            BinOp.MULTIPLY: builder.mul,
            BinOp.DIVIDE: builder.sdiv,
            BinOp.MODULO: builder.srem
        }

        try:
            method = operation_to_method[node.operation]
        except KeyError:
            def compare_and_upcast(left, right):
                return builder.zext(builder.icmp_signed(node.operation, left, right), ir.IntType(64))

            method = compare_and_upcast

        return method(left, right)

    if isinstance(node, UnOp):
        def logical_not(value):
            """!a is 1 if a is 0, else 0."""
            return builder.zext(builder.icmp_signed('==', value, ir.Constant(ir.IntType(64), 0)), ir.IntType(64))

        operation_to_method = {UnOp.MINUS: builder.neg, UnOp.COMPLEMENT: builder.not_, UnOp.PLUS: lambda v: v,
                               UnOp.NOT: logical_not}

        method = operation_to_method[node.operation]
        value = to_llvm(node.operand, builder, module)
        return method(value)
    if isinstance(node, Wrap):
        module = ir.Module('generated', )
        module.triple = "x86_64-unknown-linux-gnu"
        for statement in node.children:
            to_llvm(statement, builder, module=module)
        return module
    if isinstance(node, String):
        return string_to_llvm(node)

    if isinstance(node, Identifier):
        try:
            if (node.name.find("[") > 0):
                index1 = node.name.find("[") + 1
                index2 = node.name.find("]")
                varr = node.name[index1: index2]
                try:
                    varr = int(varr)
                except:
                    var = llvm_converter_state.identifier_to_var[
                        str(node.name).replace(varr, str(dictr[varr]))]
            else:
                var = llvm_converter_state.identifier_to_var[node.name]
        except KeyError:
            return builder.function.args[llvm_converter_state.arg_identifiers_to_index[node.name]]

        return builder.load(var)
    if isinstance(node, If):
        predicate = condition_to_llvm(node.condition, builder, module)
        if node.else_block is None:
            with builder.if_then(predicate) as then:
                to_llvm(node.if_block, builder, module)
        else:
            with builder.if_else(predicate) as (then, otherwise):
                with then:
                    to_llvm(node.if_block, builder, module)
                with otherwise:
                    to_llvm(node.else_block, builder, module)

    if isinstance(node, ForLoop):
        cond_varname = 'forcond'
        to_llvm(node.for_init, builder, module)
        with builder.for_loop(cond_varname) as (condition, incr, loop):
            with condition:
                condition_to_llvm(node.for_condition, builder,
                                  module, varname=cond_varname)
            with incr:
                to_llvm(node.for_increment, builder, module)
            with loop:
                to_llvm(node.for_body, builder, module)


def condition_to_llvm(node, builder: CustomBuilder, module, varname=''):
    condition = to_llvm(node, builder, module)

    if isinstance(condition.type, ir.IntType):
        return builder.icmp_signed('!=', to_llvm(node, builder, module), ir.Constant(ir.IntType(64), 0), name=varname)
    else:
        raise NotImplementedError(
            'Lazy developer does not implement what does not crash')


def integer_to_llvm(node: Integer):
    i_type = ir.IntType(64)
    return ir.Constant(i_type, node.value)
