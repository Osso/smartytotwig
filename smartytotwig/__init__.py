import fileinput

from smartytotwig.smarty_grammar import smarty_language
from smartytotwig.pyPEG import parse, parseLine, parser


def parse_file(file_name, language=smarty_language):
    """
    Parse a smarty template file.
    """
    file_input = fileinput.FileInput(file_name)
    return parse(language, file_input, False)


def parse_string(text, language=smarty_language):
    """
    Parse a Smarty template string.
    """
    p = parser()
    result, text = p.parseLine(text, language, [], False)
    return result[0][1] # Don't return the 'smarty_language' match.
