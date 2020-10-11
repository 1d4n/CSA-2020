import json


def lca(pair):
    """
    Return the Lowest-Common-Anccestor of 2 nodes in a binary tree
    Args:
        a pair of 2 indexes in the tree [i, j]
    """
    high = max(pair)
    low = min(pair)
    equal = high == low
    
    if not equal:
        if high % 2 == 0:
            high = (high - 2) // 2
            pair = [high, low]
        else:
            high = (high - 1) // 2
            pair = [high, low]
    else:
        return pair[0]
    
    return lca(pair)


if __name__ == '__main__':
    with open('tree.txt', 'r') as tree_file:
        tree = tree_file.read()

    with open('pairs.txt', 'r') as pairs_file:
        pairs_list = json.load(pairs_file)

    flag = ''.join([tree[lca(pair)] for pair in pairs_list])
    print("The flag is:", flag)
