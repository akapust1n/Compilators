from antlr_ast.ast import AstNode, BaseNodeTransformer
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


class Transformer(BaseNodeTransformer):
    def visit_BinaryExpr(self, node):
        return BinaryExpr.from_spec(node)

    def visit_SubExpr(self, node):
        return SubExpr.from_spec(node)

    def visit_NotExpr(self, node):
        return NotExpr.from_spec(node)

    def visit_Terminal(self, node):
        return node.get_text()