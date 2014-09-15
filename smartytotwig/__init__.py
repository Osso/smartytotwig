import fileinput
import pypeg2

from .smarty_grammar import SmartyLanguage


def parse_file(file_name, language=SmartyLanguage):
    """
    Parse a smarty template file.
    """
    file_input = fileinput.FileInput(file_name)
    return pypeg2.parse(file_input, language, whitespace="")


def parse_string(text, language=SmartyLanguage):
    """
    Parse a Smarty template string.
    """
    return pypeg2.parse(text, language, whitespace="")
