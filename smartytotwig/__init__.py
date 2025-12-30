from typing import Any

import pypeg2

from .smarty_grammar import SmartyLanguageMainOrEmpty


def parse_file(file_name: str, language: type = SmartyLanguageMainOrEmpty) -> Any:
    """
    Parse a smarty template file.
    """
    with open(file_name, encoding="utf-8") as f:
        return pypeg2.parse(f.read(), language, filename=file_name, whitespace="")


def parse_string(text: str, language: type = SmartyLanguageMainOrEmpty) -> Any:
    """
    Parse a Smarty template string.
    """
    return pypeg2.parse(text, language, whitespace="")
