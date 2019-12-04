#!/usr/bin/python3

import string


def meet_criteria_part1(number):
    for d in string.digits:
        if number.count(d * 2) > 0:
            return True

    return False


def meet_criteria_part2(number):
    for d in string.digits:
        if number.count(d * 2) == 1 and \
           number.count(d * 3) == 0:
            return True

    return False


def get_passwords_count(start, end, criteria_func):
    count = 0
    for d1 in range(int(str(start)[0]), int(str(end)[0]) + 1):
        for d2 in range(d1, 10):
            for d3 in range(d2, 10):
                for d4 in range(d3, 10):
                    for d5 in range(d4, 10):
                        for d6 in range(d5, 10):
                            number = '%d'*6 % (d1, d2, d3, d4, d5, d6)
                            if int(number) < start:
                                continue
                            elif int(number) > end:
                                return count
                            elif criteria_func(number):
                                count += 1


# Part 1 - Main
print('Part 1 answer: {0}'.format(
      get_passwords_count(146810, 612564, meet_criteria_part1)))

# Part 2 - Main
print('Part 2 answer: {0}'.format(
      get_passwords_count(146810, 612564, meet_criteria_part2)))
