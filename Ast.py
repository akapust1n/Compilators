from antlr_ast.ast import AstNode
from antlr_py.CVisitor import CVisitor


class SubExpr(AstNode):
    _fields = ['expr->expression']


class BinaryExpr(AstNode):
    _fields = ['left', 'right', 'op']


class NotExpr(AstNode):
    _fields = ['NOT->op', 'expr']

class AstVisitor(CVisitor):
    def visitBinaryExpr(self, ctx):
        return BinaryExpr._from_fields(self, ctx)