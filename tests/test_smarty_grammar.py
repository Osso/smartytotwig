"""
It's easy to screw up other rules when modifying the underlying grammar.
These unit tests test various smarty statements, to make refactoring the
grammar more sane.
"""
from smartytotwig import parse_string
from smartytotwig.twig_printer import TwigPrinter


def convert_code(smarty_code):
    ast = parse_string(smarty_code)
    print 'ast', ast
    return ast.accept(TwigPrinter())


def test_print_symbol():
    r = convert_code("{$foo}")
    assert r == "{{ foo }}"


def test_print_symbol_no_filter():
    r = convert_code("{$foo nofilter}")
    assert r == '{{ foo|raw }}'


def test_whitespace_before():
    r = convert_code("{   $foo}")
    assert r == "{{ foo }}"


def test_print_whitespace_after():
    r = convert_code("{$foo   }")
    assert r == "{{ foo }}"


def test_print_func():
    r = convert_code("{foo|bar:param1}")
    assert r == "{{ foo|bar(param1) }}"


def test_print_func_array():
    r = convert_code("{foo|bar:param1['hello']}")
    assert r == "{{ foo|bar(param1['hello']) }}"


def test_print_func_array_num():
    r = convert_code("{foo|bar:param1[4]}")
    assert r == "{{ foo|bar(param1[4]) }}"


def test_print_single_quoted_string():
    r = convert_code("{'foo'}")
    assert r == "{{ 'foo' }}"


def test_print_double_quoted_string():
    r = convert_code('{"foo"}')
    assert r == '{{ "foo" }}'


def test_print_double_quoted_string_no_filter():
    r = convert_code('{"foo" nofilter}')
    assert r == '{{ "foo"|raw }}'


def test_print_variable_double_quoted_string():
    r = convert_code('{"$foo"}')
    assert r == '{{ "${foo}" }}'


def test_print_variable_double_quoted_string_no_filter():
    r = convert_code('{"$foo" nofilter}')
    assert r == '{{ "${foo}"|raw }}'


def test_print_variable_single_quoted_string():
    r = convert_code("{'$foo'}")
    assert r == "{{ '$foo' }}"


def test_print_object_dereference():
    r = convert_code('{$foo->hello}')
    assert r == '{{ foo.hello }}'


def test_print_object_dereference_2():
    r = convert_code('{$foo.hello}')
    assert r == '{{ foo.hello }}'


def test_print_object_dereference_variables():
    r = convert_code('{$foo.$hello}')
    assert r == '{{ foo.hello }}'


def test_print_object_dereference_method():
    r = convert_code('{$foo.hello()}')
    assert r == '{{ foo.hello() }}'


def test_print_object_dereference_composed():
    r = convert_code('{$foo.bar.hello}')
    assert r == '{{ foo.bar.hello }}'


def test_print_object_dereference_composed_variables():
    r = convert_code('{$foo.$bar.$hello}')
    assert r == '{{ foo.bar.hello }}'


def test_print_string_object_dereference():
    r = convert_code('{"$foo->hello"}')
    assert r == '{{ "${foo.hello}" }}'


def test_print_string_object_dereference_2():
    r = convert_code('{"$foo.hello"}')
    assert r == '{{ "${foo.hello}" }}'


def test_if_statement():
    r = convert_code("{if foo}\nhello\n{/if}")
    assert r == "{% if foo %}\nhello\n{% endif %}"


def test_if_not_statement():
    r = convert_code("{if !foo}\nhello\n{/if}")
    assert r == "{% if not foo %}\nhello\n{% endif %}"


def test_if_and_statement():
    r = convert_code("{if foo and bar}\nhello\n{/if}")
    assert r == "{% if foo and bar %}\nhello\n{% endif %}"


def test_if_or_statement():
    r = convert_code("{if foo or bar}\nhello\n{/if}")
    assert r == "{% if foo or bar %}\nhello\n{% endif %}"


def test_if_equal_statement():
    r = convert_code("{if foo == bar}\nhello\n{/if}")
    assert r == "{% if foo == bar %}\nhello\n{% endif %}"


def test_if_not_equal_statement():
    r = convert_code("{if foo != bar}\nhello\n{/if}")
    assert r == "{% if foo != bar %}\nhello\n{% endif %}"


def test_if_lower_statement():
    r = convert_code("{if foo < bar}\nhello\n{/if}")
    assert r == "{% if foo < bar %}\nhello\n{% endif %}"


def test_if_lower_or_equal_statement():
    r = convert_code("{if foo <= bar}\nhello\n{/if}")
    assert r == "{% if foo <= bar %}\nhello\n{% endif %}"


def test_if_greater_statement():
    r = convert_code("{if foo > bar}\nhello\n{/if}")
    assert r == "{% if foo > bar %}\nhello\n{% endif %}"


def test_if_greater_or_equal_statement():
    r = convert_code("{if foo >= bar}\nhello\n{/if}")
    assert r == "{% if foo >= bar %}\nhello\n{% endif %}"

def test_if_instanceof():
    r = convert_code("{if foo instanceof bar}\nhello\n{/if}")
    assert r == "{% if foo is bar %}\nhello\n{% endif %}"


def test_if_func_statement():
    r = convert_code("{if foo($bar)}\nhello\n{/if}")
    assert r == "{% if foo(bar) %}\nhello\n{% endif %}"


def test_if_func_no_param_statement():
    r = convert_code("{if foo()}\nhello\n{/if}")
    assert r == "{% if foo() %}\nhello\n{% endif %}"


def test_if_variable_dereference():
    r = convert_code("{if foo.bar}\nhello\n{/if}")
    assert r == "{% if foo.bar %}\nhello\n{% endif %}"


def test_if_variable_dereference_2():
    r = convert_code("{if foo->bar}\nhello\n{/if}")
    assert r == "{% if foo.bar %}\nhello\n{% endif %}"


def test_if_variable_dereference_3():
    r = convert_code("{if $foo.bar}\nhello\n{/if}")
    assert r == "{% if foo.bar %}\nhello\n{% endif %}"


def test_if_variable_dereference_4():
    r = convert_code("{if $foo->bar}\nhello\n{/if}")
    assert r == "{% if foo.bar %}\nhello\n{% endif %}"


def test_if_array():
    r = convert_code("{if foo['bar']}\nhello\n{/if}")
    assert r == "{% if foo['bar'] %}\nhello\n{% endif %}"


def test_if_filter():
    r = convert_code("{if foo|bar}\nhello\n{/if}")
    assert r == "{% if foo|bar %}\nhello\n{% endif %}"


def test_if_func_multiple_params_statement():
    r = convert_code("{if foo($bar1, $bar2)}\nhello\n{/if}")
    assert r == "{% if foo(bar1, bar2) %}\nhello\n{% endif %}"


def test_if_func_var_params_statement():
    r = convert_code("{if foo($bar1, $bar2)}\nhello\n{/if}")
    assert r == "{% if foo(bar1, bar2) %}\nhello\n{% endif %}"


def test_if_statement_multiple():
    """Test an if statement (no else or elseif)"""
    r = convert_code(
        "{if !foo or foo.bar or foo|bar:foo['hello']}\nfoo\n{/if}")
    assert r == "{% if not foo or foo.bar or foo|bar(foo['hello']) %}\nfoo\n{% endif %}"


def test_if_else_statement():
    """Test an an if with an else and a single logical operation."""
    r = convert_code("{if foo}\nbar\n{else}\nfoo{/if}")
    assert r == "{% if foo %}\nbar\n{% else %}\nfoo{% endif %}"


def test_if_elseif_statement():
    """Test an an if with an elseif."""
    r = convert_code(
        "{if foo}\nbar\n{elseif blue}\nfoo{/if}")
    assert r == "{% if foo %}\nbar\n{% elseif blue %}\nfoo{% endif %}"


def test_if_filter_statement():
    """Test an an if with an else and an elseif and two logical operations."""
    r = convert_code(
        "{if awesome.string|banana:\"foo\\\" $a\"}\nbar\n{/if}")
    assert r == "{% if awesome.string|banana(\"foo\\\" ${a}\") %}\nbar\n{% endif %}"


def test_if_and_filter_statement():
    """Test an an if with an else and an elseif and two logical operations."""
    r = convert_code(
        "{if foo and awesome.string|banana:\"foo\\\" $a\"}\nbar\n{/if}")
    assert r == "{% if foo and awesome.string|banana(\"foo\\\" ${a}\") %}\nbar\n{% endif %}"


def test_if_string_statement():
    """Test an an if with an else and an elseif and two logical operations."""
    r = convert_code(
        "{if 'hello'}\nbar\n{/if}")
    assert r == "{% if 'hello' %}\nbar\n{% endif %}"


def test_if_elseif_and_statement():
    """Test an an if with an else and an elseif and two logical operations."""
    r = convert_code(
        "{if foo}\nbar\n{elseif awesome.sauce[1] and blue and 'hello'}\nfoo{/if}")
    assert r == "{% if foo %}\nbar\n{% elseif awesome.sauce[1] and blue and 'hello' %}\nfoo{% endif %}"


def test_if_not_array_statement():
    r = convert_code(
        "{if !foo[3]}\nbar\n{/if}")
    assert r == "{% if not foo[3] %}\nbar\n{% endif %}"


def test_if_elseif_else_statement():
    """Test an if with an elseif and else clause."""
    r = convert_code(
        "{if foo}\nbar\n{elseif blue}\nfoo\n{else}bar{/if}")
    assert r == "{% if foo %}\nbar\n{% elseif blue %}\nfoo\n{% else %}bar{% endif %}"


def test_if_paren_statement():
    """Test an an if statement with parenthesis."""
    r = convert_code(
        "{if (foo and bar) or foo and (bar or (foo and bar))}\nbar\n{else}\nfoo{/if}")
    assert r == "{% if (foo and bar) or foo and (bar or (foo and bar)) %}\nbar\n{% else %}\nfoo{% endif %}"


def test_if_elseif_paren_statement():
    """Test an an elseif statement with parenthesis."""
    r = convert_code(
        "{if foo}\nbar\n{elseif (foo and bar) or foo and (bar or (foo and bar))}\nfoo{/if}")
    assert r == "{% if foo %}\nbar\n{% elseif (foo and bar) or foo and (bar or (foo and bar)) %}\nfoo{% endif %}"


def test_if_variable_statement():
    """Test an an elseif statement with parenthesis."""
    r = convert_code(
        "{if $foo}\nbar\n{/if}")
    assert r == "{% if foo %}\nbar\n{% endif %}"


def test_function_statement():
    """Test a a simple function statement."""
    r = convert_code("{foo arg1=bar arg2=3}")
    assert r == "{{ {'arg1': bar, 'arg2': 3}|foo }}"


def test_function_statement2():
    """Test a a simple function statement with object and array arguments."""
    r = convert_code(
        "{foo arg1=bar[1] arg2=foo.bar.foo arg3=foo.bar[3] arg4=foo.bar.awesome[3] }")
    assert r == "{{ {'arg1': bar[1], 'arg2': foo.bar.foo, 'arg3': foo.bar[3], 'arg4': foo.bar.awesome[3]}|foo }}"


def test_function_statement_at_operator():
    """Test a a simple function statement."""
    r = convert_code("{@foo arg1=bar arg2=3}")
    assert r == "{{ {'arg1': bar, 'arg2': 3}|foo }}"


def test_function_statement3():
    """Test a function statement with modifiers in in the parameters."""
    r = convert_code(
        "{foo arg1=bar[1]|modifier arg2=foo.bar.foo arg3=foo.bar[3]|modifier:array[0]:\"hello $foo \" arg4=foo.bar.awesome[3]|modifier2:7:'hello':\"hello\":\"`$apple.banana`\"}")
    assert r == "{{ {\'arg1\': bar[1]|modifier, \'arg2\': foo.bar.foo, \'arg3\': foo.bar[3]|modifier(array[0], \"hello ${foo} \"), \'arg4\': foo.bar.awesome[3]|modifier2(7, \'hello\', \"hello\", \"${apple.banana}\")}|foo }}"


def test_for_statement():
    """Test a a simple foreach statement."""
    r = convert_code(
        "{foreach $foo as $bar}content{/foreach}")
    assert r == "{% for bar in foo %}content{% endfor %}"


def test_old_for_statement():
    """Test a a simple foreach statement."""
    r = convert_code(
        "{foreach item=bar from=foo}content{/foreach}")
    assert r == "{% for bar in foo %}content{% endfor %}"


def test_old_for_statement_whitespace():
    """Test a a simple foreach statement."""
    r = convert_code(
        "{foreach item=bar from=foo }content{/foreach}")
    assert r == "{% for bar in foo %}content{% endfor %}"


def test_old_for_statement_name():
    """Test a more complex foreach statement."""
    r = convert_code(
        "{foreach item='bar'    name=snuh key=\"foobar\" from=foo[5].bar[2]|hello:\"world\":\" $hey \" }bar{/foreach}")
    assert r == "{% for bar in foo[5].bar[2]|hello(\"world\", \" ${hey} \") %}bar{% endfor %}"


def test_old_for_statement_foreachelse():
    """Test a for statement with a foreachelse clause."""
    r = convert_code(
        "{foreach item='bar' name=snuh key=\"foobar\" from=foo.bar[2]|hello:\"world\":\" $hey \" }bar{foreachelse}{if !foo}bar{/if}hello{/foreach}")
    assert r == "{% for bar in foo.bar[2]|hello(\"world\", \" ${hey} \") %}bar{% else %}{% if not foo %}bar{% endif %}hello{% endfor %}"


def test_content():
    r = convert_code("hello")
    assert r == 'hello'


def test_comment():
    r = convert_code("{* hello *}")
    assert r == '{# hello #}'


def test_literal():
    r = convert_code("{literal}{foo}{/literal}")
    assert r == '{foo}'


def test_variable_underscore():
    r = convert_code("{$news_item}")
    assert r == '{{ news_item }}'


def test_variable_dereference_filter_nofilter():
    r = convert_code("{$newsitem.parsed_body|html_substr:250 nofilter}")
    assert r == '{{ "%s"|format(newsitem.parsed_body|html_substr(250)) }}'


def test_variable_dereference_filter_nofilter():
    r = convert_code("{$newsitem.parsed_body|html_substr:250}")
    assert r == '{{ newsitem.parsed_body|html_substr(250) }}'


def test_for_iteration():
    r = convert_code("{foreach $foo as $bar}{$bar@iteration}{/foreach}")
    assert r == '{% for bar in foo %}{{ loop.index }}{% endfor %}'


def test_for_iteration_expression():
    r = convert_code("{foreach $foo as $bar}{$bar@iteration+1}{/foreach}")
    assert r == '{% for bar in foo %}{{ loop.index + 1 }}{% endfor %}'


def test_for_multiline():
    r = convert_code(
        "{foreach $foo as $bar}\nhello\n{$bar@iteration}\n{/foreach}")
    assert r == "{% for bar in foo %}\nhello\n{{ loop.index }}\n{% endfor %}"


def test_translation():
    r = convert_code('{t id="hello"}')
    assert r == '{% t "hello" %}'


def test_translation_variable():
    r = convert_code('{t id=$hello}')
    assert r == '{% t hello %}'


def test_translation_islink():
    r = convert_code('{t id="hello" quoted=true}')
    assert r == '{% t "hello" islink %}'


def test_javascript():
    r = convert_code("{ dateFormat: 'yy-mm-dd' }")
    assert r == "{ dateFormat: 'yy-mm-dd' }"


def test_include():
    r = convert_code('{include file="foo/bar.tpl"}')
    assert r == '{% include "foo/bar.twig" %}'


def test_empty():
    r = convert_code("")
    assert r == ''


def test_assign():
    r = convert_code("{assign var=cache_get_queries value=$cache}")
    assert r == '{% set cache_get_queries = cache %}'


def test_assign_function():
    r = convert_code("{assign var=cache_get_queries value=$cache->get_get_queries()}")
    assert r == '{% set cache_get_queries = cache.get_get_queries() %}'

def test_simple_tag():
    r = convert_code("{init_time}")
    assert r == '{{ init_time() }}'
