# Smarty to Twig

[![CI](https://github.com/osso/smartytotwig/actions/workflows/test.yml/badge.svg)](https://github.com/osso/smartytotwig/actions/workflows/test.yml)

Converts Smarty 3 templates to Twig templates.

Based on https://github.com/freshrichard/smartytotwig

## Installation

```bash
pip install git+https://github.com/osso/smartytotwig.git
```

Or for development:

```bash
git clone https://github.com/osso/smartytotwig.git
cd smartytotwig
uv sync
```

## Usage

```bash
smartytotwig --smarty-file=examples/guestbook.tpl --twig-file=output.twig
```

## Supported Features

- Variables: `{$foo}` → `{{ foo }}`
- Object/array access: `{$foo->bar}`, `{$foo.bar}`, `{$foo['key']}`
- Modifiers/filters: `{$foo|bar:param}` → `{{ foo|bar(param) }}`
- nofilter: `{$foo nofilter}` → `{{ foo|raw }}`
- If/elseif/else statements
- Foreach loops with loop variables (`@iteration`, `@index`, `@total`, `@key`)
- Foreachelse
- Comments: `{* comment *}` → `{# comment #}`
- Literal blocks: `{literal}...{/literal}`
- Include: `{include file="foo.tpl"}` → `{% include "foo.twig" %}`
- Assign: `{assign var=x value=y}` → `{% set x = y %}`
- Delimiter tags: `{ldelim}`, `{rdelim}`
- Comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`, `eq`, `ne`, `neq`, `gt`, `lt`
- Logical operators: `and`, `or`, `&&`, `||`, `!`
- instanceof: `{if $foo instanceof Bar}` → `{% if foo is Bar %}`
- Function calls with parameters

## Requirements

- Python 3.9+
