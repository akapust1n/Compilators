from antlr4 import *
#from . import antlr_py as grammar
from antlr_py.CLexer import CLexer
from antlr_py.CListener import CListener
from antlr_py.CParser import CParser
from Ast import AstVisitor
from antlr_ast.ast import parse as parse_ast, process_tree


#def parse(text, start="expr", **kwargs):
#    antlr_tree = parse_ast(grammar, text, start, upper=False, **kwargs)
#    simple_tree = process_tree(antlr_tree, transformer_cls=Transformer)

#    return simple_tree


def main():
    with open("samples/factorial.c", "r") as file:
        code = file.read()
        stream = InputStream(code)
        lexer = CLexer(stream)
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        #visitor = AstVisitor()

        token = lexer.nextToken()
        print(token)
        while (token.text != "<EOF>"):
            token = lexer.nextToken()
            print(token)


if __name__ == '__main__':
    main()
