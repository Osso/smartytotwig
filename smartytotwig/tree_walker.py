import re


def node_type(node):
    return node[0]


def node_ast(node):
    return node[1]


class Node(object):
    def __init__(self, _type, ast):
        self.type = _type
        self.ast = ast

    @classmethod
    def from_dict(cls, ast):
        return Node(node_type(ast), node_ast(ast))


# Stores the actual visitor methods
def make_visitor():
    _methods = {}

    # The actual @visitor decorator
    def _visitor(arg_type):
        """Decorator that creates a visitor method."""

        # Delegating visitor implementation
        def _visitor_impl(self, arg, *args, **kwargs):
            """Actual visitor method implementation."""
            method = _methods[arg.type]
            # method = _methods[type(arg)]
            return method(self, arg.ast , *args, **kwargs)

        def decorator(fn):
            _methods[arg_type] = fn
            # Replace all decorated methods with _visitor_impl
            return _visitor_impl

        return decorator

    return _visitor


class TreeWalker(object):

    """
    Takes an AST of a parsed smarty program
    and returns the parsed Twig template. This
    is meant as a helper it does not understand 100%
    of the Smarty synatx.
    """

    # Lookup tables for performing some token
    # replacements not addressed in the grammar.
    replacements = {
        r'smarty\.foreach.*\.index': 'loop.index0',
        r'smarty\.foreach.*\.iteration': 'loop.index'
    }

    keywords = {
        'foreachelse': '{% else %}',
        'else': '{% else %}',
    }

    visitor = make_visitor()

    def __init__(self, visitor, twig_extension="", twig_path=""):
        """
        The AST structure is created by pyPEG.
        """
        self.visitor = visitor
        self.twig_extension = 'twig'
        self.twig_path = ''

        if twig_extension:
            self.twig_extension = twig_extension

        if twig_path:
            self.twig_path = twig_path

    def walk(self, ast):
        # Top level handler for walking the tree.
        return self.walk_ast(ast)

    def visit_ast(self, ast):
        node = Node(node_type(ast), ast)
        return self.visitor.visit(node)

    def visit_node(self, node):
        return self.visitor.visit(node)

    @visitor('comment')
    def visit(self, ast):
        return "{#%s#}" % ast[2:-2]

    @visitor('function_parameter')
    def visit(self, ast):
        symbol = self.visit(Node.from_dict(ast[0]))
        expression = self.visit(Node.from_dict(ast[1]))
        return (symbol, expression)

    @visitor('exp_no_modifier')
    def visit(self, ast):
        return self.walk_ast(ast)

    @visitor('junk')
    def visit(self, ast):
        return ""

    @visitor('smarty_language')
    def visit(self, ast):
        """
        The entry-point for the parser.
        contains a set of top-level smarty
        statements.
        """
        return self.walk_ast(ast)

    @visitor('left_paren')
    def visit(self, ast):
        return "("

    @visitor('right_paren')
    def visit(self, ast):
        return ")"

    @visitor('and_operator')
    def visit(self, ast):
        """
        &&, and operator in Smarty.
        """
        return ' and '

    @visitor('or_operator')
    def visit(self, ast):
        """
        ||, or, operator in Smarty.
        """
        return ' or '

    @visitor('equals_operator')
    def visit(self, ast):
        """
        eq, == opeartor in Smarty.
        """
        return ' == '

    @visitor('ne_operator')
    def visit(self, ast):
        """
        ne, neq, != opeartor in Smarty.
        """
        return ' != '

    @visitor('lt_operator')
    def visit(self, ast):
        """
        < operator in smarty.
        """
        return ' < '

    @visitor('lte_operator')
    def visit(self, ast):
        """
        <= operator in smarty.
        """
        return ' <= '

    @visitor('gt_operator')
    def visit(self, ast):
        """
        > operator in smarty.
        """
        return ' > '

    @visitor('gte_operator')
    def visit(self, ast):
        """
        >= operator in smarty.
        """
        return ' >= '

    def walk_ast(self, ast):
        def visit_el(el):
            if isinstance(el, tuple):
                node = Node.from_dict(el)
                return self.visit(node)
            elif isinstance(el, str):
                return el
            else:
                raise Exception()
        return "".join(visit_el(el) for el in ast)

    @visitor('literal')
    def visit(self, ast):
        """
        A literal block in smarty, we can just
        drop the {literal} tags because Twig
        is less ambiguous.
        """
        return self.visit_node(Node('literal', ast))

    @visitor('variable_string')
    def visit(self, ast):
        """
        A complex string containing variables, e.x.,

            "`$foo.bar` Hello World $bar"

        """

        code = "\""

        # Crawl through the ast snippet and create a
        # string in the format "%s%s%s"
        # and a set of the parameters that will be
        # outputted with this string.
        variables = []
        string_contents = ''
        for k, v in ast:
            # Plain-text.
            if k == 'text':
                string_contents += "".join(v)
            # An expression.
            else:
                string_contents += "%s"
                expression = self.visit(Node('expression', v))
                variables.append(expression)

        # Now insert all the parameters
        function_params_string = ', '.join(v for v in variables)

        # The final string outputted is in the format:
        #
        #   "%s text %s"|format(foo, bar)
        #
        # format is a Twig modifier similar to sprintf.
        if len(function_params_string):
            code = "%s%s\"|format(%s)" % (
                code,
                string_contents,
                function_params_string
            )
        else:  # Deal with parsing error on double-quoted strings.
            code = "%s%s\"" % (code, string_contents)

        return code

    @visitor('function_statement')
    def visit(self, ast):
        """
        Smarty functions are mapped to a modifier in
        Twig with a hash as input.
        """
        code = ""

        # The variable that starts a function statement.
        function_name = self.visit(Node.from_dict(ast[0]))
        # Cycle through the function_parameters and store them
        # these will be passed into the modifier as a dictionary.
        function_params = [self.visit(Node(k, v)) for k, v in ast[1:]]

        # Deal with the special case of an include function in
        # smarty this should be mapped onto Twig's include tag.
        if function_name == 'include' and 'file' in function_params:
            tokens = function_params['file'].split('/')
            file_name = tokens[len(tokens) - 1]
            file_name = "%s/%s.%s" % (
                self.twig_path,
                re.sub(r'\..*$', '', file_name),
                self.twig_extension
            )
            code += "%s{%% include \"%s\" %%}" % file_name
            return code

        # Now create a dictionary string from the paramters.
        function_params_string = '[%s]' % \
            ", ".join("'%s': %s" % (k, v)
                      for k, v in function_params)

        code += "{{ %s|%s }}" % (
            function_params_string,
            function_name
        )
        return code

    @visitor('print_statement')
    def visit(self, ast):
        """
        A print statement in smarty includes:

        {foo}
        {foo|bar:parameter}
        """

        # Walking the expression that starts a
        # modifier statement.
        expression = self.walk_ast(ast)

        # Perform any keyword replacements if found.
        if expression in self.keywords:
            return self.keywords[expression]

        return "{{ %s }}" % expression

    @visitor('modifier')
    def visit(self, ast):
        """
        A modifier statement:

        foo|bar:a:b:c
        """
        return self.walk_ast(ast)

    @visitor('modifier_right')
    def visit(self, ast):
        """
        The right-hand side of the modifier
        statement:

        bar:a:b:c
        """
        code = "|"

        code += self.walk_ast(ast[:1])

        # We must have parameters being passed
        # in to the modifier.
        if len(ast) > 1:
            code += "(%s)" % (
                ", ".join(self.walk_ast([node])
                          for node in ast[1:])
            )

        return code

    @visitor('content')
    def visit(self, ast):
        """
        Raw content, e.g.,

        <html>
            <body>
                <b>Hey</b>
            </body>
        </html>
        """
        return ast

    @visitor('for_statement')
    def visit(self, ast):
        """
        A foreach statement in smarty:

        {foreach from=expression item=foo}
        {foreachelse}
        {/foreach}
        """

        code = "{% for "

        for_parts = {}
        for k, v in ast:
            for_parts[k] = v

        if 'foreach_array' in for_parts:
            code += "%s in %s" % (self.walk_ast([for_parts['foreach_array'][1]]),
                                  self.walk_ast([for_parts['foreach_array'][0]]))
            ast = ast[1:]

        # What variable is the for data being stored as.
        if 'for_item' in for_parts:
            code += "%s " % self.walk_ast(for_parts['for_item'])
            ast = ast[1:]

        # What is the for statement reading from?
        if 'for_from' in for_parts:
            code += "in %s" % self.walk_ast(for_parts['for_from'])
            ast = ast[1:]

        if 'for_key' in for_parts:
            ast = ast[1:]

        if 'for_name' in for_parts:
            ast = ast[1:]

        code = "%s %%}" % code

        # The content inside the if statement.
        # Else and elseif statements.
        code += self.walk_ast(ast)

        return '%s{%% endfor %%}' % code

    @visitor('junk')
    def visit(self, ast):
        return ""

    @visitor('if_statement')
    def visit(self, ast):
        """
        An if statement in smarty:

        {if expression (operator expression)}
        {elseif expression (operator expression)}
        {else}
        {/if}
        """
        code = "{% if "

        # Walking the expressions in an if statement.
        for node in ast:
            if node_type(node) == 'smarty_language':
                break
            code += self.walk_ast([node])
            ast = ast[1:]

        code += " %}"

        # The content inside the if statement.
        code += self.walk_ast([ast[0]])

        # Else and elseif statements.
        code += self.walk_ast(ast[1:])

        code += '{% endif %}'
        return code

    @visitor('elseif_statement')
    def visit(self, ast):
        """
        The elseif part of an if statement, essentially
        this is the same as an if statement but without
        the elseif or else part.

        {elseif expression (operator expression)}
        """
        return "{%% elseif %s %%}%s" % (
            # Walking the expressions in an if statement.
            self.walk_ast(ast[:-1]),
            # The content inside the if statement.
            self.walk_ast(ast[-1:])
        )

    @visitor('foreachelse_statement')
    def visit(self, ast):
        """
        The foreachelse part of a for loop.
        """
        return "{%% else %%}%s" % self.walk_ast(ast)

    @visitor('else_statement')
    def visit(self, ast):
        """
        The else part of an if statement.
        """
        return "{%% else %%}%s" % self.walk_ast(ast)

    @visitor('operator')
    def visit(self, ast):
        """
        Operators in smarty.
        """
        # Evaluate the different types of expressions.
        return self.walk_ast(ast)

    @visitor('func_params')
    def visit(self, ast):
        """
        function parameters in smary:
        bar1,bar2
        bar1, bar2
        """
        return ", ".join(self.walk_ast([node])
                         for node in ast if node_type(node) != 'junk')

    @visitor('func_call')
    def visit(self, ast):
        """
        A function call in smarty:
        foo(bar)
        """
        return "%s%s" % (self.walk_ast(ast[:1]), self.walk_ast(ast[1:]))

    @visitor('expression')
    def visit(self, ast):
        """
        A top level expression in Smarty that statements
        are built out of mostly expressions and/or symbols (which are
        encompassed in the expression type.
        """
        # Evaluate the different types of expressions.
        expression = self.walk_ast(ast)

        # Should we perform any replacements?
        for k, v in self.replacements.items():
            if re.match(k, expression):
                expression = v
                break

        return expression

    @visitor('object_dereference')
    def visit(self, ast):
        """
        An object dereference expression in Smarty:

        foo.bar
        """
        left, right = ast
        return "%s.%s" % (self.walk_ast([left]), self.walk_ast([right]))

    @visitor('array')
    def visit(self, ast):
        """
        An array expression in Smarty:

        foo[bar]
        """
        left, right = ast
        return "%s[%s]" % (self.walk_ast([left]), self.walk_ast([right]))

    @visitor('string')
    def visit(self, ast):
        """
        A string in Smarty:
        "hello"
        """
        return ''.join(ast)

    @visitor('dollar_symbol')
    def visit(self, ast):
        """
        A variable in Smarty:
        $foo
        """
        return self.walk_ast([('symbol', ast)])

    @visitor('identifier')
    def visit(self, ast):
        """
        A identifier in Smarty:
        foo
        """
        return ast

    @visitor('symbol')
    def visit(self, ast):
        """
        A symbol (variable) in Smarty, e.g,

        !foobar
        foo_bar
        foo3
        $foo
        """
        variable = self.walk_ast(ast[-1:])

        # Is there a ! operator.
        if node_type(ast[0]) == 'not_operator':
            variable = "not %s" % variable
        elif node_type(ast[0]) == 'at_operator':
            pass  # Nom nom, at operators are not supported in Twig

        return variable
