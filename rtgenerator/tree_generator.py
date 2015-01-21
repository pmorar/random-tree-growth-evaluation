__author__ = 'Pavel Morar <pvmorar@gmail.com>'

import numpy.random as random


class Tree:

    class Node:
        def __init__(self):
            self.weight = 1
            self.height = 1
            self.tree_weight = 1
            self.children  = []

        def add_children(self, n):
            self.weight += 1
            self.tree_weight += n + 1
            if self.height == 1:
                self.height = 2
            for i in xrange(n):
                self.children.append(Tree.Node())

        def __str__(self):
            return "(%d, %d, %d)" % (self.weight, self.tree_weight, self.height)

    def __init__(self):
        self.root = Tree.Node()

    def height(self):
        return self.root.height

    def add_children_to_random_node(self, n):
        r = self.root
        rnd = 1 + random.randint(0, r.tree_weight)
        self._add(n, r, rnd, 0)

    def _add(self, n, node, rnd, cum_sum):
        if rnd > cum_sum + node.tree_weight:
            return None, cum_sum + node.tree_weight

        cum_sum += node.weight
        if cum_sum >= rnd:
            node.add_children(n)
            return node.height + 1, None

        for child in node.children:
            h, cum_sum = self._add(n, child, rnd, cum_sum)
            if h is not None:
                node.tree_weight += 1 + n
                node.height = max(node.height, h)
                return node.height + 1, None

        raise AssertionError("We should have added children!")


def generate_random_tree_height(children_num_generator, num_steps):
    tree = Tree()
    for i in xrange(num_steps):
        tree.add_children_to_random_node(children_num_generator())
    return tree.height()

if __name__ == '__main__':
    print generate_random_tree_height(lambda: 1, 10)