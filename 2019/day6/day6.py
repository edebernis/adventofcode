#!/usr/bin/python3


def build_tree(tree, node, orbits):
    tree[node] = {}
    if node not in orbits:
        return
    orbits_nodes = orbits[node]
    del orbits[node]
    for orbit in orbits_nodes:
        build_tree(tree[node], orbit, orbits)

    return tree


def calc_direct_indirects_orbits(tree, depth=0, count=0):
    for k in tree.keys():
        count += depth
        count += calc_direct_indirects_orbits(tree[k], depth=depth + 1)
    return count


def find(tree, value, depth=0):
    for k in tree.keys():
        if k == value:
            return depth
    for k in tree.keys():
        res = find(tree[k], value, depth=depth + 1)
        if res:
            return res


def calc_minimum_orbit_transfers(tree, transfers):
    res1 = find(tree, 'SAN')
    res2 = find(tree, 'YOU')
    if None in (res1, res2):
        return min(transfers)

    transfers.append(res1 + res2)
    return min([calc_minimum_orbit_transfers(tree[k], transfers)
                for k in tree.keys()])


# Part 1 - Test cases
orbits = {
    'COM': ['B'],
    'B': ['C', 'G'],
    'C': ['D'],
    'D': ['E', 'I'],
    'E': ['F', 'J'],
    'G': ['H'],
    'J': ['K'],
    'K': ['L']
}
tree = build_tree({}, 'COM', orbits)
assert calc_direct_indirects_orbits(tree) == 42

# Part 2 - Test cases
orbits = {
    'COM': ['B'],
    'B': ['C', 'G'],
    'C': ['D'],
    'D': ['E', 'I'],
    'E': ['F', 'J'],
    'G': ['H'],
    'I': ['SAN'],
    'J': ['K'],
    'K': ['L', 'YOU']
}
tree = build_tree({}, 'COM', orbits)
assert calc_minimum_orbit_transfers(tree['COM'], []) == 4

# Part 1 and 2 - Main
orbits = {}
for line in [line.strip().split(')')
             for line in open('input_part1').readlines()]:
    if line[0] in orbits:
        orbits[line[0]].append(line[1])
    else:
        orbits[line[0]] = [line[1]]
tree = build_tree({}, 'COM', orbits)
print('Part 1 answer: {0}'.format(
      calc_direct_indirects_orbits(tree)))
print('Part 2 answer: {0}'.format(
      calc_minimum_orbit_transfers(tree['COM'], [])))
