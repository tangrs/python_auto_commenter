import ast, sys # import modules ast and sys

f = open(__file__, 'r') # set f to the return value of calling open
file_tree = ast.parse(f.read()) # set file_tree to the return value of calling parse on ast

comments = [] # set comments to an empty list

def add_comment(comment, node): # define a function called add_comment
	global comments # comments is a global variable
	comments.append((node.lineno, comment)) # no idea what's happening here

#################################################
#
#  Stringifies
#
#################################################

def stringify_list(node): # define a function called stringify_list
	if (len(node.elts) < 1): # if the return value of calling len is less than 1 is true then # no idea what's happening here
		return "an empty list" # return "an empty list"

	return "a list" # return "a list"

def stringify_tuple(node): # define a function called stringify_tuple
	strings = [stringify(el) for el in node.elts]

	if (len(strings) < 1): # if the return value of calling len is less than 1 is true then # no idea what's happening here
		return "empty tuple" # return "empty tuple"

	return "tuple of " + " and ".join(strings) # return from the function

def stringify_name(node): # define a function called stringify_name
	return node.id # return id

def stringify_num(node): # define a function called stringify_num
	return str(node.n) # return the return value of calling str

def stringify_str(node): # define a function called stringify_str
	return '"{}"'.format(node.s) # return the return value of calling format on ""{}""

def stringify_boolop(node): # define a function called stringify_boolop
	op_str = {
		ast.And: " and ",
		ast.Or:  " or "
	}[type(node.op)]

	return op_str.join([stringify(v) for v in node.values]) # return the return value of calling join on op_str

def stringify_dict(node): # define a function called stringify_dict
	if (len(node.keys) < 1): # if the return value of calling len is less than 1 is true then # no idea what's happening here
		return "an empty dictionary" # return "an empty dictionary"
	return "a dictionary" # return "a dictionary"

def stringify_attribute(node): # define a function called stringify_attribute
	return node.attr # return attr

def stringify_call(node): # define a function called stringify_call
	# this is a pseudo statement. this only called when return value ignored
	function_str = stringify(node.func) # set function_str to the return value of calling stringify

	if (function_str == None): # if function_str is equal to None is true then # no idea what's happening here
		function_str = "this function" # set function_str to "this function"

	if (type(node.func) == ast.Attribute): # if the return value of calling type is equal to Attribute is true then # no idea what's happening here
		function_str = function_str + " on " + stringify(node.func.value)

	return "the return value of calling " + function_str # return from the function

def stringify_compare(node): # define a function called stringify_compare
	comp_ops = { # set comp_ops to a dictionary
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

	left_expr = stringify(node.left) # set left_expr to the return value of calling stringify
	right_expr = [stringify(comp) for comp in node.comparators]
	ops_str = [comp_ops[type(op)] for op in node.ops]

	ops_right_pairs = zip(ops_str, right_expr) # set ops_right_pairs to the return value of calling zip
	right_expr = " which ".join(["is {} {}".format(pair[0], pair[1]) for pair in ops_right_pairs]) # set right_expr to the return value of calling join on " which "


	return left_expr + " " + right_expr # return from the function

stringify_handlers = { # set stringify_handlers to a dictionary
	ast.List:		stringify_list,
	ast.Str:		stringify_str,
	ast.Tuple:		stringify_tuple,
	ast.Name:		stringify_name,
	ast.Num:		stringify_num,
	ast.Dict:		stringify_dict,
	ast.BoolOp:		stringify_boolop,
	ast.Call:		stringify_call,
	ast.Attribute:	stringify_attribute,
	ast.Compare:	stringify_compare
}

def stringify(node): # define a function called stringify
	try: # no idea what's happening here
		return stringify_handlers[type(node)](node)
	except KeyError:
		# print "Unhandled!!", type(node), node.lineno
		return None

#################################################
#
#  Statements
#
#################################################

def handle_assign(node): # define a function called handle_assign
	assigns = " and ".join([stringify(k) for k in node.targets]) # set assigns to the return value of calling join on " and "
	value = stringify(node.value) # set value to the return value of calling stringify
	comment = "set {} to {}".format(assigns, value) # set comment to the return value of calling format on "set {} to {}"

	if (value != None): # if value is not equal to None is true then # no idea what's happening here
		add_comment(comment, node) # no idea what's happening here

def handle_while(node): # define a function called handle_while
	expr_str = stringify(node.test) # set expr_str to the return value of calling stringify
	comment = "while {} is true".format(expr_str) # set comment to the return value of calling format on "while {} is true"

	if (expr_str != None): # if expr_str is not equal to None is true then # no idea what's happening here
		add_comment(comment, node) # no idea what's happening here

	annotate(node) # no idea what's happening here

def handle_if(node): # define a function called handle_if
	expr_str = stringify(node.test) # set expr_str to the return value of calling stringify
	comment = "if {} is true then".format(expr_str) # set comment to the return value of calling format on "if {} is true then"

	if (expr_str != None): # if expr_str is not equal to None is true then # no idea what's happening here
		add_comment(comment, node) # no idea what's happening here

	annotate(node) # no idea what's happening here

def handle_function(node): # define a function called handle_function
	comment = "define a function called " + node.name
	add_comment(comment, node) # no idea what's happening here

	annotate(node) # no idea what's happening here

def handle_call(node): # define a function called handle_call
	# this is a pseudo statement. this only called when return value ignored
	comment = "call the function " + stringify(node.func)
	add_comment(comment, node) # no idea what's happening here

def handle_return(node): # define a function called handle_return
	value_str = stringify(node.value) # set value_str to the return value of calling stringify
	comment = "return " # set comment to "return "

	if (value_str != None): # if value_str is not equal to None is true then # no idea what's happening here
		comment += value_str # no idea what's happening here
	else:
		comment += "from the function" # no idea what's happening here

	add_comment(comment, node) # no idea what's happening here

def handle_import(node): # define a function called handle_import
	comment = "import modules " # set comment to "import modules "
	modules = [alias.name for alias in node.names]

	comment += " and ".join(modules) # no idea what's happening here
	add_comment(comment, node) # no idea what's happening here

def handle_pass(node): # define a function called handle_pass
	add_comment("do nothing", node) # no idea what's happening here

def handle_print(node): # define a function called handle_print
	add_comment("print message to screen", node) # no idea what's happening here

def handle_global(node): # define a function called handle_global
	comment = " and ".join(node.names) # set comment to the return value of calling join on " and "

	if (len(node.names) > 1): # if the return value of calling len is greater than 1 is true then # no idea what's happening here
		comment += " are global variables" # no idea what's happening here
	else:
		comment += " is a global variable" # no idea what's happening here

	add_comment(comment, node) # no idea what's happening here

statement_handlers = { # set statement_handlers to a dictionary
	ast.Assign: 		handle_assign,
	ast.While:			handle_while,
	ast.If:				handle_if,
	ast.FunctionDef:	handle_function,
	ast.Call:			handle_call,
	ast.Return:			handle_return,
	ast.Import:			handle_import,
	ast.Pass:			handle_pass,
	ast.Global:			handle_global
}


def annotate(tree): # define a function called annotate
	for node in ast.iter_child_nodes(tree): # no idea what's happening here
		if type(node) in statement_handlers.keys():
			statement_handlers[type(node)](node)
		else:
			#print "Unhandled!!", type(node),
			if ("lineno" in node._attributes):
				#print "on line", node.lineno
				add_comment("no idea what's happening here", node)
			else:
				pass
				#print

annotate(file_tree) # no idea what's happening here

f.seek(0) # no idea what's happening here
modified_lines = f.readlines() # set modified_lines to the return value of calling readlines on f
modified_lines = [line.rstrip('\n') for line in modified_lines]

for (line, comment) in comments: # no idea what's happening here
	modified_lines[line-1] += " # " + comment

print "\n".join(modified_lines) # no idea what's happening here

while 1 and 0: # while 1 and 0 is true # no idea what's happening here
	pass # do nothing
a=1 # set a to 1
if a == 2 < 3: # if a is equal to 2 which is less than 3 is true then # no idea what's happening here
	pass # do nothing
