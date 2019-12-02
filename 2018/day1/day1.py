#!/usr/bin/python3


class Frequency:
   def __init__(self):
      self.current_freq = 0
      self.all_freqs = {self.current_freq}

   @staticmethod
   def apply_freq_changes(changes):
       return sum(map(int, changes))

   def process_changes(self, changes):
       while True:
           for change in changes:
               self.current_freq += int(change)
               if self.current_freq in self.all_freqs:
                   return self.current_freq
               self.all_freqs.add(self.current_freq)


# Part 1 - Test cases
assert Frequency.apply_freq_changes('+1, +1, +1'.split(',')) == 3
assert Frequency.apply_freq_changes('+1, +1, -2'.split(',')) == 0
assert Frequency.apply_freq_changes('-1, -2, -3'.split(',')) == -6

# Part 1 - Main
print('Part 1 answer: {0}'.format(
	Frequency.apply_freq_changes(open('input_part1').readlines())))

# Part 2 - Test cases
assert Frequency().process_changes('+1, -1'.split(',')) == 0
assert Frequency().process_changes('+3, +3, +4, -2, -4'.split(',')) == 10
assert Frequency().process_changes('-6, +3, +8, +5, -6'.split(',')) == 5
assert Frequency().process_changes('+7, +7, -2, -7, -4'.split(',')) == 14

# Part 2 - Main
print('Part 2 answer: {0}'.format(
       Frequency().process_changes(open('input_part1').readlines())))

