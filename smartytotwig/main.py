import optparse
import sys

from . import parse_file
from .twig_printer import TwigPrinter


def main():

    opt1 = optparse.make_option(
        "-s",
        "--smarty-file",
        action="store",
        dest="source",
        help="Path to the source Smarty file."
    )

    opt2 = optparse.make_option(
        "-t",
        "--twig-file",
        action="store",
        dest="target",
        help="Location of the Twig output file."
    )

    opt3 = optparse.make_option(
        "-p",
        "--twig-path",
        action="store",
        dest="path",
        help="The path used in Twig include tags."
    )

    opt4 = optparse.make_option(
        "-e",
        "--twig-extension",
        action="store",
        dest="extension",
        help="The extension that should be used when including files in Twig."
    )

    parser = optparse.OptionParser(usage='smartytotwig'
                                         ' --smarty-file=<SOURCE TEMPLATE>'
                                         ' --twig-file=<OUTPUT TEMPLATE>')
    parser.add_option(opt1)
    parser.add_option(opt2)
    parser.add_option(opt3)
    parser.add_option(opt4)
    options, dummy_args = parser.parse_args(sys.argv)

    if options.source:
        if not options.target:
            options.target = "%s.twig" % options.source.replace('.tpl', '')

        ast = parse_file(options.source)
        out = ast.accept(TwigPrinter())
        with open(options.target, 'w+') as f:
            f.write(out)

        print 'Template outputted to %s' % options.target


if __name__ == "__main__":
    main()
