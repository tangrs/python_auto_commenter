import ast, sys

f = open(__file__, 'r')
file_tree = ast.parse(f.read())

comments = []

def add_comment(comment, node):
    global comments
    comments.append((node.lineno, comment))

#################################################
#
#  Stringifies
#
#################################################

def stringify_list(node):
    if (len(node.elts) < 1):
        return "an empty list"

    return "a list"

def stringify_tuple(node):
    strings = [stringify(el) for el in node.elts]

    if (len(strings) < 1):
        return "empty tuple"

    return "tuple of " + " and ".join(strings)

def stringify_name(node):
    return node.id

def stringify_num(node):
    return str(node.n)

def stringify_str(node):
    return '"{}"'.format(node.s)

def stringify_boolop(node):
    op_str = {
        ast.And: " and ",
        ast.Or:  " or "
    }[type(node.op)]

    return op_str.join([stringify(v) for v in node.values])

def stringify_dict(node):
    if (len(node.keys) < 1):
        return "an empty dictionary"
    return "a dictionary"

def stringify_attribute(node):
    return node.attr

def stringify_call(node):
    # this is a pseudo statement. this only called when return value ignored
    function_str = stringify(node.func)

    if (function_str == None):
        function_str = "this function"

    if (type(node.func) == ast.Attribute):
        function_str = function_str + " on " + stringify(node.func.value)

    return "the return value of calling " + function_str

def stringify_compare(node):
    comp_ops = {
        ast.Eq: "equal to",
        ast.NotEq:  "not equal to",
        ast.Lt: "less than",
        ast.LtE: "less than or equal to",
        ast.Gt: "greater than",
        ast.GtE: "greater than or equal to",
        ast.Is: "",
        ast.IsNot: "not",
        ast.In: "in",
        ast.NotIn: "not in"
    }

    left_expr = stringify(node.left)
    right_expr = [stringify(comp) for comp in node.comparators]
    ops_str = [comp_ops[type(op)] for op in node.ops]

    ops_right_pairs = zip(ops_str, right_expr)
    right_expr = " which ".join(["is {} {}".format(pair[0], pair[1]) for pair in ops_right_pairs])


    return left_expr + " " + right_expr

stringify_handlers = {
    ast.List:       stringify_list,
    ast.Str:        stringify_str,
    ast.Tuple:      stringify_tuple,
    ast.Name:       stringify_name,
    ast.Num:        stringify_num,
    ast.Dict:       stringify_dict,
    ast.BoolOp:     stringify_boolop,
    ast.Call:       stringify_call,
    ast.Attribute:  stringify_attribute,
    ast.Compare:    stringify_compare
}

def stringify(node):
    try:
        return stringify_handlers[type(node)](node)
    except KeyError:
        print "Unhandled!!", type(node), node.lineno
        return None

#################################################
#
#  Statements
#
#################################################

def handle_assign(node):
    assigns = " and ".join([stringify(k) for k in node.targets])
    value = stringify(node.value)
    comment = "set {} to {}".format(assigns, value)

    if (value != None):
        add_comment(comment, node)

def handle_while(node):
    expr_str = stringify(node.test)
    comment = "while {} is true".format(expr_str)

    if (expr_str != None):
        add_comment(comment, node)

    annotate(node)

def handle_if(node):
    expr_str = stringify(node.test)
    comment = "if {} is true then".format(expr_str)

    if (expr_str != None):
        add_comment(comment, node)

    annotate(node)

def handle_function(node):
    comment = "define a function called " + node.name
    add_comment(comment, node)

    annotate(node)

def handle_call(node):
    # this is a pseudo statement. this only called when return value ignored
    comment = "call the function " + stringify(node.func)
    add_comment(comment, node)

def handle_return(node):
    value_str = stringify(node.value)
    comment = "return "

    if (value_str != None):
        comment += value_str
    else:
        comment += "from the function"

    add_comment(comment, node)

def handle_import(node):
    comment = "import modules "
    modules = [alias.name for alias in node.names]

    comment += " and ".join(modules)
    add_comment(comment, node)

def handle_importfrom(node):
    names = " and ".join([alias.name for alias in node.names])
    module = node.module
    comment = "import {} from the {} module".format(names, module)
    add_comment(comment, node)

def handle_pass(node):
    add_comment("do nothing", node)

def handle_print(node):
    add_comment("print message to screen", node)

def handle_global(node):
    comment = " and ".join(node.names)

    if (len(node.names) > 1):
        comment += " are global variables"
    else:
        comment += " is a global variable"

    add_comment(comment, node)

statement_handlers = {
    ast.Assign:         handle_assign,
    ast.While:          handle_while,
    ast.If:             handle_if,
    ast.FunctionDef:    handle_function,
    ast.Call:           handle_call,
    ast.Return:         handle_return,
    ast.Import:         handle_import,
    ast.ImportFrom:     handle_importfrom,
    ast.Pass:           handle_pass,
    ast.Global:         handle_global,
    ast.Print:          handle_print
}


def annotate(tree):
    for node in ast.iter_child_nodes(tree):
        if type(node) in statement_handlers.keys():
            statement_handlers[type(node)](node)
        else:
            print "Unhandled!!", type(node),
            if ("lineno" in node._attributes):
                print "on line", node.lineno
                add_comment("no idea what's happening here", node)
            else:
                pass
                print

annotate(file_tree)

f.seek(0)
modified_lines = f.readlines()
modified_lines = [line.rstrip('\n') for line in modified_lines]

for (line, comment) in comments:
    modified_lines[line-1] += " # " + comment

print "\n".join(modified_lines)

while 1 and 0:
    pass
a = 1
if a == 2 < 3:
    pass
