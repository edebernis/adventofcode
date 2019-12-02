#!/usr/bin/python3


class Computer:
   def __init__(self):
      self.opcode_pos = None
   
   def run_program(self, program):
      self.opcode_pos = 0
      while program[self.opcode_pos] != 99:
         self._run(program)

      return program
   
   def _run(self, program):
      input1_pos = program[self.opcode_pos + 1]
      input2_pos = program[self.opcode_pos + 2]
      output_pos = program[self.opcode_pos + 3]
     
      try:
         {
             1: self._add,
             2: self._multiply
         }[program[self.opcode_pos]](program, input1_pos,
                                     input2_pos, output_pos)
      except KeyError:
         raise Exception('Something went wrong')
     
      self.opcode_pos += 4 

   def _add(self, program, input1_pos, input2_pos, output_pos):
      program[output_pos] = program[input1_pos] + program[input2_pos]

   def _multiply(self, program, input1_pos, input2_pos, output_pos):
      program[output_pos] = program[input1_pos] * program[input2_pos]


# Part 1 - Test cases
computer = Computer()
assert computer.run_program([1,0,0,0,99]) == [2,0,0,0,99]
assert computer.run_program([2,3,0,3,99]) == [2,3,0,6,99]
assert computer.run_program([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
assert computer.run_program([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

# Part 1 - Main
program = list(map(int, open('input_part1').read().split(',')))
program[1] = 12
program[2] = 2
Computer().run_program(program)
print("Part 1 answer: {0}".format(program[0]))

# Part 2 - Main
initial_program = list(map(int, open('input_part1').read().split(',')))
computer = Computer()
for noun in range(100):
   for verb in range(100):
       program = initial_program.copy()
       program[1] = noun
       program[2] = verb
       computer.run_program(program)
       if program[0] == 19690720:
           print("Part 2 answer: {0}".format(100 * noun + verb))
           break

