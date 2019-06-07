import click as click

from lexer import parse, read_grammar, to_ast
from llvm_backend import to_llvm

with open('C_grammar', 'r') as f:
    g = read_grammar(f.read())


# @click.Parameter()   # nice to get the docs on signature/parameters that click.argument does not give easily.
def compile(source_file):
    token_list, remainder = parse(g, source_file.read())
    print(remainder)
    assert remainder.strip() == '', 'Failed to parse!'
    print("win parse!")
    ast = to_ast(token_list)
    print(to_llvm(ast))


if __name__ == '__main__':
    with open("myex.c") as file:
        compile(file)
