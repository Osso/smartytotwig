"""
It's easy to screw up other rules when modifying the underlying grammar.
These unit tests test various smarty statements, to make refactoring the
grammar more sane.
"""
import smartytotwig

from smartytotwig.tree_walker import TreeWalker


def convert_code(smarty_code):
    ast = smartytotwig.parse_string(smarty_code)
    tree_walker = TreeWalker(ast)
    return tree_walker.code


def test_print_symbol():
    r = convert_code("{$foo}")
    assert r == "{{ foo }}"


def test_print_func():
    r = convert_code("{foo|bar:param1}")
    assert r == "{{ foo|bar(param1) }}"


def test_print_func_array():
    r = convert_code("{foo|bar:param1['hello']}")
    assert r == "{{ foo|bar(param1['hello']) }}"


def test_print_string():
    r = convert_code("{'foo'}")
    assert r == "{{ 'foo' }}"


def test_print_string2():
    r = convert_code('{"foo"}')
    assert r == '{{ "foo" }}'


def test_print_variable_string():
    r = convert_code('{"$foo"}')
    assert r == '{{ "%s"|format(foo) }}'


def test_if_statement():
    r = convert_code(
        "{if foo}\nhello\n{/if}")
    assert r == "{% if foo %}\nhello\n{% endif %}"


def test_if_and_statement():
    r = convert_code(
        "{if foo and bar}\nhello\n{/if}")
    assert r == "{% if foo and bar %}\nhello\n{% endif %}"


def test_if_or_statement():
    r = convert_code(
        "{if foo or bar}\nhello\n{/if}")
    assert r == "{% if foo or bar %}\nhello\n{% endif %}"


def test_if_equal_statement():
    r = convert_code(
        "{if foo == bar}\nhello\n{/if}")
    assert r == "{% if foo == bar %}\nhello\n{% endif %}"


def test_if_not_equal_statement():
    r = convert_code(
        "{if foo != bar}\nhello\n{/if}")
    assert r == "{% if foo != bar %}\nhello\n{% endif %}"


def test_if_lower_statement():
    r = convert_code(
        "{if foo < bar}\nhello\n{/if}")
    assert r == "{% if foo < bar %}\nhello\n{% endif %}"


def test_if_lower_or_equal_statement():
    r = convert_code(
        "{if foo <= bar}\nhello\n{/if}")
    assert r == "{% if foo <= bar %}\nhello\n{% endif %}"


def test_if_greater_statement():
    r = convert_code(
        "{if foo > bar}\nhello\n{/if}")
    assert r == "{% if foo > bar %}\nhello\n{% endif %}"


def test_if_greater_or_equal_statement():
    r = convert_code(
        "{if foo >= bar}\nhello\n{/if}")
    assert r == "{% if foo >= bar %}\nhello\n{% endif %}"


def test_if_statement1():
    """Test an if statement (no else or elseif)"""
    r = convert_code(
        "{if !foo or foo.bar or foo|bar:foo['hello']}\nfoo\n{/if}")
    assert r == "{% if not foo or foo.bar or foo|bar(foo['hello']) %}\nfoo\n{% endif %}"


def test_if_statement2():
    """Test an an if with an else and a single logical operation."""
    r = convert_code("{if foo}\nbar\n{else}\nfoo{/if}")
    assert r == "{% if foo %}\nbar\n{% else %}\nfoo{% endif %}"


def test_if_statement3():
    """Test an an if with an else and an elseif and two logical operations."""
    r = convert_code(
        "{if foo and awesome.string|banana:\"foo\\\" $a\"}\nbar\n{elseif awesome.sauce[1] and blue and 'hello'}\nfoo{/if}")
    assert r == "{% if foo and awesome.string|banana(\"foo\\\" %s\"|format(a)) %}\nbar\n{% elseif awesome.sauce[1] and blue and \'hello\' %}\nfoo{% endif %}"


def test_if_statement4():
    """Test an if with an elseif and else clause."""
    r = convert_code(
        "{if foo|bar:3 or !foo[3]}\nbar\n{elseif awesome.sauce[1] and blue and 'hello'}\nfoo\n{else}bar{/if}")
    assert r == "{% if foo|bar(3) or not foo[3] %}\nbar\n{% elseif awesome.sauce[1] and blue and 'hello' %}\nfoo\n{% else %}bar{% endif %}"


def test_if_statement5():
    """Test an an if statement with parenthesis."""
    r = convert_code(
        "{if (foo and bar) or foo and (bar or (foo and bar))}\nbar\n{else}\nfoo{/if}")
    assert r == "{% if (foo and bar) or foo and (bar or (foo and bar)) %}\nbar\n{% else %}\nfoo{% endif %}"


def test_if_statement6():
    """Test an an elseif statement with parenthesis."""
    r = convert_code(
        "{if foo}\nbar\n{elseif (foo and bar) or foo and (bar or (foo and bar))}\nfoo{/if}")
    assert r == "{% if foo %}\nbar\n{% elseif (foo and bar) or foo and (bar or (foo and bar)) %}\nfoo{% endif %}"


def test_function_statement():
    """Test a a simple function statement."""
    r = convert_code("{foo arg1=bar arg2=3}")
    assert r == "{{ ['arg1': bar, 'arg2': 3]|foo }}"


def test_function_statement2():
    """Test a a simple function statement with object and array arguments."""
    r = convert_code(
        "{foo arg1=bar[1] arg2=foo.bar.foo arg3=foo.bar[3] arg4=foo.bar.awesome[3] }")
    assert r == "{{ ['arg1': bar[1], 'arg2': foo.bar.foo, 'arg3': foo.bar[3], 'arg4': foo.bar.awesome[3]]|foo }}"


def test_function_statement3():
    """Test a function statement with modifiers in in the parameters."""
    r = convert_code(
        "{foo arg1=bar[1]|modifier arg2=foo.bar.foo arg3=foo.bar[3]|modifier:array[0]:\"hello $foo \" arg4=foo.bar.awesome[3]|modifier2:7:'hello':\"hello\":\"`$apple.banana`\"}")
    assert r == "{{ [\'arg1\': bar[1]|modifier, \'arg2\': foo.bar.foo, \'arg3\': foo.bar[3]|modifier(array[0], \"hello %s \"|format(foo)), \'arg4\': foo.bar.awesome[3]|modifier2(7, \'hello\', \"hello\", \"%s\"|format(apple.banana))]|foo }}"


def test_for_statement():
    """Test a a simple foreach statement."""
    r = convert_code(
        "{foreach $foo as $bar}{/foreach}")
    assert r == "{% for bar in foo %}{% endfor %}"


def test_old_for_statement():
    """Test a a simple foreach statement."""
    r = convert_code(
        "{foreach item=bar from=foo}{/foreach}")
    assert r == "{% for bar in foo %}{% endfor %}"


def test_old_for_statement1():
    """Test a a simple foreach statement."""
    r = convert_code(
        "{foreach item=bar from=foo }{/foreach}")
    assert r == "{% for bar in foo %}{% endfor %}"


def test_old_for_statement2():
    """Test a more complex foreach statement."""
    r = convert_code(
        "{foreach item='bar'    name=snuh key=\"foobar\" from=foo[5].bar[2]|hello:\"world\":\" $hey \" }bar{/foreach}")
    assert r == "{% for bar in foo[5].bar[2]|hello(\"world\", \" %s \"|format(hey)) %}bar{% endfor %}"


def test_old_for_statement3():
    """Test a for statement with a foreachelse clause."""
    r = convert_code(
        "{foreach item='bar'    name=snuh key=\"foobar\" from=foo.bar[2]|hello:\"world\":\" $hey \" }bar{foreachelse}{if !foo}bar{/if}hello{/foreach}")
    assert r == "{% for bar in foo.bar[2]|hello(\"world\", \" %s \"|format(hey)) %}bar{% else %}{% if not foo %}bar{% endif %}hello{% endfor %}"


def test_content():
    r = convert_code("hello")
    assert r == 'hello'


def test_comment():
    r = convert_code("{* hello *}")
    assert r == '{# hello #}'


def test_literal():
    r = convert_code("{literal}{foo}{/literal}")
    assert r == '{foo}'
