from antlr_ast import AstNode
from CVisitor import CVisitor


class SubExpr(AstNode):
    _fields = ['expr->expression']


class BinaryExpr(AstNode):
    _field = ['left', 'right', 'op']


class NotExpr(AstNode):
    _fields = ['NOT->op', 'expr']

class AstVisitor(CVisitor):
    def visitBinaryExpr(self, ctx):
        return BinaryExpr._from_fields(self, ctx)