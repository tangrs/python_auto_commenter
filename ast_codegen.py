import ast, sys

with open(__file__, 'r') as f:
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

stringify_handlers = {
	ast.List:		stringify_list,
	ast.Str:		stringify_str,
	ast.Tuple:		stringify_tuple,
	ast.Name:		stringify_name,
	ast.Num:		stringify_num,
	ast.Dict:		stringify_dict,
	ast.BoolOp:		stringify_boolop,
	ast.Call:		stringify_call,
	ast.Attribute:	stringify_attribute
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
	comment = "while {} is true, do the following".format(expr_str)

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
	comment = "return"
	if (value_str != None):
		comment += " " + value_str

	add_comment(comment, node)

def handle_import(node):
	comment = "import the following module"
	modules = [alias[0] for alias in node.names]
	if (len(modules) > 1):
		comment += 's'

	comment += ": " + " and ".join(modules)
	add_comment(comment, node)

statement_handlers = {
	ast.Assign: 		handle_assign,
	ast.While:			handle_while,
	ast.FunctionDef:	handle_function,
	ast.Call:			handle_call,
	ast.Return:			handle_return,
	ast.Import:			handle_import
}


def annotate(tree):
	for node in ast.iter_child_nodes(tree):
		if type(node) in statement_handlers.keys():
			statement_handlers[type(node)](node)
		else:
			print "Unhandled!!", type(node)

annotate(file_tree)
print "\n".join([str(c) for c in comments])

while 1 and 0:
	pass