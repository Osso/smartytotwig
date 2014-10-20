import fileinput
import pypeg2

from .smarty_grammar import SmartyLanguageMain


def parse_file(file_name, language=SmartyLanguageMain):
    """
    Parse a smarty template file.
    """
    with open(file_name) as f:
        return pypeg2.parse(f.read(), language, filename=file_name, whitespace="")


def parse_string(text, language=SmartyLanguageMain):
    """
    Parse a Smarty template string.
    """
    return pypeg2.parse(text, language, whitespace="")
