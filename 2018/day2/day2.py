#!/usr/bin/python3


class Box:
    def __init__(self, id):
       self.id = id

    def get_letters_count(self):
        count = {}
        for l in self.id:
            if l in count:
                count[l] += 1
            else:
                count[l] = 1
        return count


def checksum(boxes):
    exactly_two = 0
    exactly_three = 0
    for box in boxes:
        counts = list(box.get_letters_count().values())
        if 2 in counts:
            exactly_two += 1
        if 3 in counts:
            exactly_three += 1
    return exactly_two * exactly_three


def find_similar_boxes(ids):
    for i in range(len(ids[0])):
        ids_minus_i = []
        for id in ids.copy():
            l = list(id)
            l.pop(i)
            ids_minus_i.append(''.join(l))
        seen = set()
        for id in ids_minus_i:
            if id in seen:
                return id
            seen.add(id)


# Part 1 - Test cases
boxes = [Box(id) for id in ['abcdef', 'bababc', 'abbcde', 'abcccd',
                            'aabcdd', 'abcdee', 'ababab']]
assert checksum(boxes) == 12

# Part 1 - Main
boxes = [Box(id) for id in open('input_part1').readlines()]
print('Part 1 answer: {0}'.format(checksum(boxes)))

# Part 2 - Test cases
ids = ['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']
assert find_similar_boxes(ids) == 'fgij'

# Part 2 - Main
ids = open('input_part1').readlines()
print('Part 2 answer: {0}'.format(find_similar_boxes(ids)))

