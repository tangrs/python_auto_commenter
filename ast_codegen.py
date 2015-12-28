import ast, sys

with open(__file__, 'r') as f:
	file_tree = ast.parse(f.read())

comments = []

def add_comment(comment, node):
	global comments
	comments.append((node.lineno, comment))

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


stringify_handlers = {
	ast.Str:		stringify_str,
	ast.Tuple:		stringify_tuple,
	ast.Name:		stringify_name,
	ast.Num:		stringify_num
}

def stringify(node):
	try:
		return stringify_handlers[type(node)](node)
	except KeyError:
		return None

def handle_assign(node):
	assigns = " and ".join([stringify(k) for k in node.targets])
	value = stringify(node.value)
	comment = "set {} to {}".format(assigns, value)

	add_comment(comment, node)

def handle_while(node):
	pass
	annotate(node)

statement_handlers = {
	ast.Assign: 	handle_assign,
	ast.While:		handle_while
}


def annotate(tree):
	for node in ast.iter_child_nodes(tree):
		try:
			statement_handlers[type(node)](node)
		except KeyError:
			pass

annotate(file_tree)