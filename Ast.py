from antlr_ast import AstNode


class SubExpr(AstNode):
    _fields = ['expr->expression']


class BinaryExpr(AstNode):
    _field = ['left', 'right', 'op']


class NotExpr(AstNode):
    _fields = ['NOT->op', 'expr']