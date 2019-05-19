from antlr4 import *
from CLexer import CLexer
from CListener import CListener
from CParser import CParser


def main():
    with open("samples/factorial.c", "r") as file:
        code = file.read()
        stream = InputStream(code)
        lexer = CLexer(stream)
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        token = lexer.nextToken()
        print(token)
        while (token.text != "<EOF>"):
            token = lexer.nextToken()
            print(token)


if __name__ == '__main__':
    main()
