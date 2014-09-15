from smartytotwig.tree_walker import make_visitor


class TwigPrinter(object):
    visitor = make_visitor()

    @visitor('literal')
    def visit(self, node):
        return node.replace('{literal}', '').replace('{/literal}', '')

    @visitor('literal')
    def visit(self, node):
        return node.replace('{literal}', '').replace('{/literal}', '')

