import json
import argparse
from pycparser import c_parser, c_generator
import sys
from toLlvm import _explain_type


def to_screen(tree, buf=sys.stdout, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):
    offset = 0
    lead = ' ' * offset
    if nodenames and _my_node_name is not None:
        buf.write(lead + tree.__class__.__name__ +
                  ' <' + _my_node_name + '>: ')
    else:
        buf.write(lead + tree.__class__.__name__ + ': ')
    if tree.attr_names:
        if attrnames:
            nvlist = [(n, getattr(tree, n)) for n in tree.attr_names]
            attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
        else:
            vlist = [getattr(tree, n) for n in tree.attr_names]
            attrstr = ', '.join('%s' % v for v in vlist)
        buf.write(attrstr)

    buf.write('\n')
    for (child_name, child) in tree.children():
        child.show(
            buf,
            offset=offset + 2,
            attrnames=attrnames,
            nodenames=nodenames,
            showcoord=showcoord,
            _my_node_name=child_name)


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--input_file", type=str,
                           default="samples/simple.c")
    args = argparser.parse_args()

    input_file = args.input_file
    output_json = input_file + ".json"
   # print("Input file: %s" % input_file)
    #print("Output json to: %s" % output_json)

    with open(input_file, "r") as file:
        code = file.read()
        parser = c_parser.CParser()
        ast = parser.parse(code)
        ast.show()
      #  for c in node:
       #     tree.visit(c)
        _explain_type(ast)
       # dictr = to_screen(ast)
        # print(dictr)
    # with open(output_json, "w") as output_file:
    #  output_file.write(json.dumps(dictr))


if __name__ == '__main__':
    main()
