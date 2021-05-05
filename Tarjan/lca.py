import json


def lca(a, b):
    """
    Finds the Lowest-Common-Ancestor of 2 nodes in a binary tree.
    :param a: index of the first node.
    :param b: index of the second node.
    :return: the index of the LCA of the nodes.
    """

    while a != b:
        if a > b:
            a = (a-1) // 2
        else:
            b = (b-1) // 2

    return a


if __name__ == '__main__':
    with open('tree.txt', 'r') as tree_file:
        tree = tree_file.read()

    with open('pairs.txt', 'r') as pairs_file:
        pairs_list = json.load(pairs_file)

    flag = ''.join([tree[lca(pair[0], pair[1])] for pair in pairs_list])
    print("The flag is:", flag)
