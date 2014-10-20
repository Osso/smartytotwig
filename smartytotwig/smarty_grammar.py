# pylint: disable=R0903

from __future__ import unicode_literals, print_function

import re

from pypeg2 import Keyword, maybe_some, some, optional, Literal, omit


class Rule(object):

    def __init__(self, args):
        self.children = args

    def accept(self, visitor):
        return visitor.visit(self, *[arg.accept(visitor) for arg in self.children])

    def __eq__(self, other):
        return type(self) == type(other) and self.children == other.args

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.children))


class UnaryRule(object):

    def __init__(self, child):
        self.child = child

    def accept(self, visitor):
        return visitor.visit(self, self.child.accept(visitor))

    def __eq__(self, other):
        return type(self) == type(other) and self.child == other.child

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.child))


class LeafRule(object):

    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit(self, self.value)

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.value))


class EmptyLeafRule(object):

    def accept(self, visitor):
        return visitor.visit(self)

    def __eq__(self, other):
        return type(self) == type(other)

    def __repr__(self):
        return '%s' % self.__class__.__name__

"""
Misc.
"""

class Content(LeafRule):
    grammar = re.compile(r'[^{]+')


class CommentStatement(LeafRule):
    grammar = re.compile(r"{\*.*?\*}", re.S)


class LiteralStatement(LeafRule):
    grammar = re.compile("{literal}.*?{/literal}", re.S)


class Whitespace(object):
    grammar = maybe_some([Literal(' '), Literal('\n'), Literal('\t')])


_ = omit(Whitespace)


class Identifier(LeafRule):
    grammar = re.compile(r'[\w\-\+]*\w')


"""
Logical Operators.
"""

class AndOperator(EmptyLeafRule):
    grammar = [Literal('and'), Literal('&&')]


class OrOperator(EmptyLeafRule):
    grammar = [Literal('or'), Literal('||')]


class EqOperator(EmptyLeafRule):
    grammar = [Literal('=='), Literal('eq')]


class NeOperator(EmptyLeafRule):
    grammar = [Literal('!='), Literal('ne'), Literal('neq')]


class GtOperator(EmptyLeafRule):
    grammar = [Literal('>'), Literal('gt')]


class LtOperator(EmptyLeafRule):
    grammar = [Literal('<'), Literal('lt')]


class LteOperator(EmptyLeafRule):
    grammar = Literal('<=')


class GteOperator(EmptyLeafRule):
    grammar = Literal('>=')


class RightParen(EmptyLeafRule):
    grammar = Literal(')')


class LeftParen(EmptyLeafRule):
    grammar = Literal('(')


class Operator(UnaryRule):
    grammar = [AndOperator, EqOperator, GteOperator, LteOperator,
               LtOperator, GtOperator, NeOperator, OrOperator]

"""
Smarty variables.
"""


class SingleQuotedString(LeafRule):
    grammar = "'", re.compile(r"([^']|\\.)*"), "'"


class DoubleQuotedString(LeafRule):
    grammar = '"', re.compile(r'([^"\$]|\\.)*'), '"'


class String(UnaryRule):
    grammar = [SingleQuotedString, DoubleQuotedString]


class Text(LeafRule):
    grammar = some([re.compile(r'[^$`"\\]+'), re.compile(r'\\.')])


class NotOperator(EmptyLeafRule):
    grammar = Literal('!')


class AtOperator(EmptyLeafRule):
    grammar = Literal('@')

class EmptyOperator(EmptyLeafRule):
    grammar = Literal('')

class Variable(UnaryRule):
    grammar = Literal('$'), Identifier

class Symbol(Rule):
    grammar = ([NotOperator, AtOperator, EmptyOperator],
               [Variable, Identifier])


class DollarSymbol(Rule):
    grammar = [NotOperator, AtOperator, EmptyOperator], Variable


class Expression(UnaryRule):
    pass


class Array(Rule):
    grammar = Symbol, "[", optional(Expression), "]"


class ObjectDereference(Rule):
    grammar = [Array, Symbol], ['.', '->'], Expression


class VariableString(Rule):
    grammar = '"', some([Text, ('`', Expression, '`'), ('$', Expression)]), '"'


class ExpNoModifier(UnaryRule):
    grammar = Literal(':'), [ObjectDereference, Array, Symbol, VariableString, String]

class ModifierParameters(Rule):
    grammar = some(ExpNoModifier)

class ModifierElement(Rule):
    grammar = ('|',
               [AtOperator, EmptyOperator],
               Identifier,
               optional(ModifierParameters))

class ModifierRight(Rule):
    grammar = some(ModifierElement)


class Modifier(Rule):
    grammar = [ObjectDereference, Array, Symbol,
               VariableString, String], ModifierRight


class FuncParams(Rule):
    grammar = Expression, some((',', _, Expression))


class FuncCall(Rule):
    grammar = Identifier, omit(LeftParen), optional([FuncParams, Expression]), omit(RightParen)


Expression.grammar = [FuncCall, Modifier, ObjectDereference,
                      Array, Symbol, String, VariableString]


"""
Smarty Statements.
"""

class SmartyLanguage(Rule):
    pass


class ElseStatement(UnaryRule):
    grammar = '{', Keyword('else'), '}', SmartyLanguage


class ForeachelseStatement(UnaryRule):
    grammar = '{', Keyword('foreachelse'), '}', SmartyLanguage


class NoFilter(EmptyLeafRule):
    grammar = Literal('nofilter')

class PrintStatement(Rule):
    grammar = ('{', _,
               optional('e '),
               [FuncCall, Modifier, ObjectDereference,
                Array, DollarSymbol, String, VariableString],
               optional(_, NoFilter),
               _, '}')


class FunctionParameter(Rule):
    grammar = Symbol, '=', Expression


class FunctionStatement(Rule):
    grammar = '{', _, Symbol, some(_, FunctionParameter), _, '}'


class ForFrom(UnaryRule):
    grammar = Keyword('from'), '=', omit(optional(['"', '\''])), Expression, omit(optional(['"', '\'']))


class ForItem(UnaryRule):
    grammar = Keyword('item'), '=', omit(optional(['"', '\''])), Symbol, omit(optional(['"', '\'']))


class ForName(UnaryRule):
    grammar = Keyword('name'), '=', omit(optional(['"', '\''])), Symbol, omit(optional(['"', '\'']))


class ForKey(UnaryRule):
    grammar = Keyword('key'), '=', omit(optional(['"', '\''])), Symbol, omit(optional(['"', '\'']))


class IfCondition(Rule):
    grammar = maybe_some(LeftParen), _, Expression, _, maybe_some(RightParen)


class IfConditionList(Rule):
    grammar = IfCondition, some(_, Operator, _, IfCondition)


class ElseifStatement(Rule):
    grammar = ('{', Keyword('elseif'), _, [IfConditionList, IfCondition], _, '}', SmartyLanguage)


class IfMoreStatement(Rule):
    grammar = some([ElseStatement, ElseifStatement])


class IfStatement(Rule):
    grammar = ('{', _, Keyword('if'), _, [IfConditionList, IfCondition], _, '}',
               SmartyLanguage, optional(IfMoreStatement), '{/', Keyword('if'), '}')


class ForeachArray(Rule):
    grammar = _, Expression, _, 'as', _, Symbol


class ForVariable(Rule):
    grammar = '{', _, Variable, '@', Identifier, _, '}'


class ForeachParameters(Rule):
    grammar = some(_, [ForFrom, ForItem, ForName, ForKey])


class ForContent(Rule):
    grammar = some([ForVariable, SmartyLanguage])


class ForStatement(Rule):
    grammar = ('{', _, Keyword('foreach'), [ForeachParameters, ForeachArray], _, '}',
               ForContent, optional(ForeachelseStatement),
               '{/', Keyword('foreach'), '}')


class TranslationStatement(UnaryRule):
    grammar = '{', _, Keyword('t'), _, Literal('id='), DoubleQuotedString, _, '}'


class LeftDelimTag(EmptyLeafRule):
    grammar = '{ldelim}'


class RightDelimTag(EmptyLeafRule):
    grammar = '{rdelim}'


class LeftDelim(EmptyLeafRule):
    grammar = '{'


"""
Finally, the actual language description.
"""

SmartyLanguage.grammar = some([LiteralStatement, TranslationStatement,
                              IfStatement, ForStatement, FunctionStatement,
                              CommentStatement, PrintStatement, Content,
                              LeftDelimTag, RightDelimTag])

class SmartyLanguageMain(Rule):
    grammar = some([LiteralStatement, TranslationStatement,
                    IfStatement, ForStatement, FunctionStatement,
                    CommentStatement, PrintStatement, Content,
                    LeftDelimTag, RightDelimTag, LeftDelim])
