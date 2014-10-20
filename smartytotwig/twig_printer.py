from __future__ import unicode_literals

from .tree_walker import make_visitor
from .smarty_grammar import (SmartyLanguage, DollarSymbol, PrintStatement,
                             Identifier, LiteralStatement, Variable, Symbol,
                             EmptyOperator, ExpNoModifier, ModifierParameters,
                             ModifierElement, ModifierRight, Modifier,
                             String, Expression, Array, SingleQuotedString,
                             DoubleQuotedString, VariableString, FuncCall,
                             ObjectDereference, Content, NoFilter, IfCondition,
                             IfStatement, IfConditionList, NotOperator,
                             AtOperator, AndOperator, OrOperator, GtOperator,
                             GteOperator, LtOperator, LteOperator, Operator,
                             EqOperator, NeOperator, FuncParams, ElseStatement,
                             CommentStatement, LiteralStatement, ForItem,
                             ForFrom, ForName, ForKey, Text, ForeachParameters,
                             ForeachelseStatement, ForStatement, ForeachArray,
                             FunctionParameter, FunctionStatement, LeftDelim,
                             ElseifStatement, LeftParen, RightParen,
                             IfMoreStatement, ForVariable, ForContent,
                             TranslationStatement, LeftDelimTag, RightDelimTag,
                             SmartyLanguageMain, SmartyLanguageMainOrEmpty,
                             ForExpression, AddOperator, SubOperator,
                             MultOperator, DivOperator, ArithmeticOperator,
                             Number, ForVariableIdentifier, IncludeStatement)


class TwigPrinter(object):
    visitor = make_visitor()

    # pylint: disable=W0613,E0102

    @visitor(SmartyLanguage)
    def visit(self, node, *children):
        """
        A variable in Smarty:
        $foo
        """
        return ''.join(children)

    @visitor(SmartyLanguageMain)
    def visit(self, node, *children):
        """
        A variable in Smarty:
        $foo
        """
        return ''.join(children)

    @visitor(SmartyLanguageMainOrEmpty)
    def visit(self, node, child):
        """
        A variable in Smarty:
        $foo
        """
        return child

    @visitor(VariableString)
    def visit(self, node, *children):
        """
        A variable in Smarty:
        $foo
        """
        def out(child_node, child):
            if isinstance(child_node, Expression):
                return "${%s}" % child
            else:
                return child

        return '"%s"' % ''.join(out(child_node, child)
                                for child_node, child
                                in zip(node.children, children))

    @visitor(NoFilter)
    def visit(self, node):
        return True

    @visitor(PrintStatement)
    def visit(self, node, child, nofilter=None):
        """
        A variable in Smarty:
        $foo
        """
        if nofilter:
            child = '"%%s"|format(%s)' % child
        return "{{ %s }}" % child

    @visitor(DollarSymbol)
    def visit(self, node, operator, variable):
        """
        A variable in Smarty:
        $foo, @$foo
        """
        if operator:
            return "%s %s" % (operator, variable)
        else:
            return variable


    @visitor(Symbol)
    def visit(self, node, left, right):
        """
        A variable or an identifier in Smarty:
        $foo or foo
        In case of @$foo
        @ is the left side
        $foo is the right side
        """
        if isinstance(node.children[0], (AtOperator, EmptyOperator)):
            return "%s%s" % (left, right)
        else:
            return "%s %s" % (left, right)

    @visitor(Array)
    def visit(self, node, left, right):
        """
        An array in Smarty:
        $foo['hello']
        """
        return "%s[%s]" % (left, right)

    @visitor(NotOperator)
    def visit(self, node):
        """
        A not in smarty:
        !foo
        """
        return 'not'

    @visitor(EmptyOperator)
    def visit(self, node):
        """
        Used when there is no operator
        """
        return ''

    @visitor(ExpNoModifier)
    def visit(self, node, child):
        return child

    @visitor(ModifierParameters)
    def visit(self, node, *children):
        return "(%s)" % ", ".join(children)

    @visitor(Variable)
    def visit(self, node, child):
        """
        A variable in Smarty:
        $foo
        """
        return child

    @visitor(Expression)
    def visit(self, node, child):
        """
        An expression in Smarty:
        $foo
        1+1
        """
        return child

    @visitor(Identifier)
    def visit(self, node, value):
        """
        An identifier in Smarty:
        foo
        """
        return value

    @visitor(LiteralStatement)
    def visit(self, node):
        """
        A literal in Smarty:
        {literal}function { console.log('hello') }{/literal}
        """
        return node.replace('{literal}', '').replace('{/literal}', '')

    @visitor(ModifierRight)
    def visit(self, node, *children):
        """
        A set of modifiers in Smarty:
        |bar
        """
        return "".join(children)

    @visitor(ModifierElement)
    def visit(self, node, modifier, identifier, parameters=None):
        """
        A modifier element in Smarty:
        |bar
        """
        if parameters:
            identifier += parameters
        return "|%s%s" % (modifier, identifier)

    @visitor(Modifier)
    def visit(self, node, left, right):
        """
        A modifier element in Smarty:
        |bar
        """
        return "%s%s" % (left, right)

    @visitor(String)
    def visit(self, node, value):
        """
        A string in Smarty:
        "foo"
        """
        return value

    @visitor(SingleQuotedString)
    def visit(self, node, value):
        """
        A single quoted string in Smarty:
        'foo'
        """
        return "'%s'" % value

    @visitor(DoubleQuotedString)
    def visit(self, node, value):
        """
        A double quoted string in Smarty:
        "foo"
        """
        return '"%s"' % value

    @visitor(ObjectDereference)
    def visit(self, node, variable, ref):
        """
        A method or property access in Smarty:
        foo->bar
        foo.bar
        """
        return '%s.%s' % (variable, ref)

    @visitor(Content)
    def visit(self, node, content):
        """
        HTML content in Smarty:
        foo->bar
        foo.bar
        """
        return content

    @visitor(FuncCall)
    def visit(self, node, func_name, parameters=None):
        if not parameters:
            parameters = ''
        return "%s(%s)" % (func_name, parameters)

    @visitor(IfCondition)
    def visit(self, node, *children):
        return ''.join(children)

    @visitor(IfConditionList)
    def visit(self, node, *children):
        return " ".join(children)

    @visitor(IfStatement)
    def visit(self, node, conditions, content, else_statement=None):
        if else_statement:
            content += else_statement
        return "{%% if %s %%}%s{%% endif %%}" % (conditions, content)

    @visitor(ElseifStatement)
    def visit(self, node, conditions, content):
        return "{%% elseif %s %%}%s" % (conditions, content)

    @visitor(LeftParen)
    def visit(self, node):
        return "("

    @visitor(RightParen)
    def visit(self, node):
        return ")"

    @visitor(AndOperator)
    def visit(self, node):
        return "and"

    @visitor(OrOperator)
    def visit(self, node):
        return "or"

    @visitor(GtOperator)
    def visit(self, node):
        return ">"

    @visitor(GteOperator)
    def visit(self, node):
        return ">="

    @visitor(LtOperator)
    def visit(self, node):
        return "<"

    @visitor(LteOperator)
    def visit(self, node):
        return "<="

    @visitor(EqOperator)
    def visit(self, node):
        return "=="

    @visitor(NeOperator)
    def visit(self, node):
        return "!="

    @visitor(Operator)
    def visit(self, node, child):
        return child

    @visitor(FuncParams)
    def visit(self, node, *children):
        return ", ".join(children)

    @visitor(ElseStatement)
    def visit(self, node, child):
        return "{%% else %%}%s" % child

    @visitor(CommentStatement)
    def visit(self, node, child):
        return "{#%s#}" % child[2:-2]

    @visitor(LiteralStatement)
    def visit(self, node, child):
        return child[9:-10]

    @visitor(ForItem)
    def visit(self, node, value):
        # Defer the hard work to the parent
        return value

    @visitor(ForFrom)
    def visit(self, node, value):
        # Defer the hard work to the parent
        return value

    @visitor(ForName)
    def visit(self, node, value):
        # Defer the hard work to the parent
        return value

    @visitor(ForKey)
    def visit(self, node, value):
        # Defer the hard work to the parent
        return value

    @visitor(Text)
    def visit(self, node, value):
        return ''.join(value)

    @visitor(ForStatement)
    def visit(self, node, parameters, content, else_statement=None):
        element = parameters[ForItem]
        iterable = parameters[ForFrom]
        if else_statement:
            content += else_statement
        return '{%% for %s in %s %%}%s{%% endfor %%}' % (element, iterable, content)

    @visitor(ForeachArray)
    def visit(self, node, iterable, element):
        return {
            ForItem: element,
            ForFrom: iterable
        }

    @visitor(ForeachParameters)
    def visit(self, node, *values):
        parameters = {}
        for child, value in zip(node.children, values):
            parameters[type(child)] = value
        return parameters

    @visitor(ForeachelseStatement)
    def visit(self, node, child):
        return '{%% else %%}%s' % child

    @visitor(FunctionParameter)
    def visit(self, node, symbol, expression):
        return "'%s': %s" % (symbol, expression)

    @visitor(FunctionStatement)
    def visit(self, node, symbol, *parameters):
        return "{{ [%s]|%s }}" % (', '.join(parameters), symbol)

    @visitor(AtOperator)
    def visit(self, node):
        return ''

    @visitor(IfMoreStatement)
    def visit(self, node, *children):
        return ''.join(children)

    @visitor(ForContent)
    def visit(self, node, *children):
        return ''.join(children)

    @visitor(ForVariable)
    def visit(self, node, loop_identifier, name, expression=None):
        mappings = {
            'index': 'loop.index0',
            'iteration': 'loop.index',
            'total': 'loop.length',
            'key': '_key',
        }
        if expression:
            return '{{ %s %s }}' % (mappings[name], expression)
        else:
            return '{{ %s }}' % mappings[name]

    @visitor(TranslationStatement)
    def visit(self, node, child):
        return '{%% t %s %%}' % child

    @visitor(LeftDelimTag)
    def visit(self, node):
        return '{'

    @visitor(LeftDelim)
    def visit(self, node):
        return '{'

    @visitor(RightDelimTag)
    def visit(self, node):
        return '}'

    @visitor(ForExpression)
    def visit(self, node, operator, number):
        return '%s %s' % (operator, number)

    @visitor(Number)
    def visit(self, node, child):
        return child

    @visitor(AddOperator)
    def visit(self, node):
        return '+'

    @visitor(SubOperator)
    def visit(self, node):
        return '-'

    @visitor(MultOperator)
    def visit(self, node):
        return '*'

    @visitor(DivOperator)
    def visit(self, node):
        return '/'

    @visitor(ArithmeticOperator)
    def visit(self, node, child):
        return child

    @visitor(ForVariableIdentifier)
    def visit(self, node, value):
        return value

    @visitor(IncludeStatement)
    def visit(self, node, filename):
        return "{%% include %s %%}" % filename.replace('.tpl', '.twig')

    # pylint: enable=W0612,E0102
