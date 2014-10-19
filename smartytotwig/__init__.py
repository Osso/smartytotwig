import fileinput
import pypeg2

from .smarty_grammar import SmartyLanguage


def parse_file(file_name, language=SmartyLanguage):
    """
    Parse a smarty template file.
    """
    with open(file_name) as f:
        return pypeg2.parse(f.read(), language, whitespace="")


def parse_string(text, language=SmartyLanguage):
    """
    Parse a Smarty template string.
    """
    return pypeg2.parse(text, language, whitespace="")
