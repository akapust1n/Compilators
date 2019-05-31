from antlr4 import *
import antlr4.tree.Tree
from antlr_py.CLexer import CLexer
from antlr_py.CParser import CParser
import json
import argparse


def handleExpression(expr, names, tabs=""):
    children = {}
    for child in expr.getChildren():
        if isinstance(child, antlr4.tree.Tree.TerminalNode):
            children[child.getText()] = names[child.symbol.type-1]
        else:
            children[type(child).__name__] = handleExpression(child, names, tabs + '-')
    return children


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--input_file", type=str, default="samples/factorial.c")
    args = argparser.parse_args()

    input_file = args.input_file
    output_json = input_file + ".json"
    print("Input file: %s" % input_file)
    print("Output json to: %s" % output_json)

    with open(input_file, "r") as file:
        code = file.read()
        stream = InputStream(code)
        lexer = CLexer(stream)
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        tree = parser.compilationUnit()
        tree = handleExpression(tree, lexer.ruleNames)
        with open(output_json, "w") as output_file:
            output_file.write(json.dumps(tree))


if __name__ == '__main__':
    main()
