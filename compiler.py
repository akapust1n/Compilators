from antlr4 import *
import antlr4.tree.Tree
from antlr_py.CLexer import CLexer
from antlr_py.CParser import CParser
import json
import argparse
from pycparser import c_parser, c_ast, parse_file
import sys


def to_screen(tree, buf=sys.stdout, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):

    children = {}
    if nodenames and _my_node_name is not None:
        str = tree.__class__.__name__+ ' <' + _my_node_name + '>: '
    else:
        str = tree.__class__.__name__+ ': '

    if tree.attr_names:
        if attrnames:
            nvlist = [(n, getattr(tree,n)) for n in tree.attr_names]
            attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
        else:
            vlist = [getattr(tree, n) for n in tree.attr_names]
            attrstr = ', '.join('%s' % v for v in vlist)
        str = str + attrstr

    if showcoord:
        str = str + ' (at %s)' % tree.coord

    for (child_name, child) in tree.children():
        children[child_name] = to_screen(
                                        child,
                                        buf,
                                        attrnames=attrnames,
                                        nodenames=nodenames,
                                        showcoord=showcoord,
                                        _my_node_name=child_name)
    result = {}
    result[str] = children
    return result


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
        #tree = handleExpression(tree, lexer.ruleNames)
        pparser = c_parser.CParser()
        ast = pparser.parse(code)
        ast.show()
        dictr = to_screen(ast)
        with open(output_json, "w") as output_file:
            output_file.write(json.dumps(dictr))


if __name__ == '__main__':
    main()
