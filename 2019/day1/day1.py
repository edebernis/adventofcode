#!/usr/bin/python


class Module:
   def __init__(self, mass):
      self.mass = int(mass)

   def get_required_fuel(self):
      return (self.mass / 3) - 2

   def get_total_required_fuel(self):
      fuel = self.get_required_fuel()
      if fuel < 0:
         return 0      
      return fuel + Module(fuel).get_total_required_fuel()
      

# Part 1 - Test cases
assert Module(12).get_required_fuel() == 2
assert Module(14).get_required_fuel() == 2
assert Module(1969).get_required_fuel() == 654
assert Module(100756).get_required_fuel() == 33583

# Part 1 - Main
modules = [Module(mass) for mass in open('input_part1').readlines()]
print('Part 1 answer : {0}'.format(sum([m.get_required_fuel() for m in modules])))

# Part 2 - Test cases
assert Module(14).get_total_required_fuel() == 2
assert Module(1969).get_total_required_fuel() == 966
assert Module(100756).get_total_required_fuel() == 50346

# Part 2 - Main
modules = [Module(mass) for mass in open('input_part2').readlines()]
print('Part 2 answer : {0}'.format(sum([m.get_total_required_fuel() for m in modules])))

