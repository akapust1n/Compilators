import click as click

from lexer import parse, read_grammar, to_ast
from llvm_backend import to_llvm
import os
import argparse
import sys


with open('C_grammar', 'r') as f:
    g = read_grammar(f.read())


def compile(source_file, genExe=False):
    token_list, remainder = parse(g, source_file.read())
    print(remainder)
    assert remainder.strip() == '', 'Failed to parse!'
    print("win parse!")
    ast = to_ast(token_list)
    bcFile = str(to_llvm(ast))
    print(bcFile)
    with open("result.ll", "w") as file:
        file.write(bcFile)
    print(genExe)
    if(genExe):
        os.system("clang result.ll")


if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='Process some integers.')
   # parser.add_argument('--genExe')
    #args = parser.parse_args()
    genExe = len(sys.argv) > 1
    with open("myex.c") as file:
        compile(file, genExe)
