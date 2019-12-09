class IntcodeProcessor:

    max_args = 3

    def __init__(self, code, inputs=None):
        self.original_code = code
        self.reset(inputs=inputs)
        self.bind_opcodes()

    def get_arg(self, index, mode):
        result = self.code[index]
        if mode == 0:
            result = self.code[result]
        elif mode == 1:
            pass
        elif mode == 2:
            result = self.code[result + self.relative_base]
        return result

    def write(self, index, value, mode):
        result = self.code[index]
        if mode == 0:
            self.code[result] = value
        elif mode == 1:
            raise ValueError
        elif mode == 2:
            self.code[result + self.relative_base] = value

    def reset(self, inputs=None):
        self.code = list(self.original_code) + [0] * 10000  # maybe fix later
        self.index = 0
        self.inputs = inputs
        self.all_outputs = []
        self.outputs = []
        self.halted = False
        self.relative_base = 0

    def run(self):
        self.all_outputs.extend(self.outputs)
        self.outputs = []
        should_suspend = False
        while not self.halted and not should_suspend:
            opcode, modes = self.parse_opcode(self.code[self.index])
            should_suspend = self.opcodes[opcode](modes)
        return self.halted, self.outputs

    def bind_opcodes(self):
        self.opcodes = {
            1: self.add,
            2: self.mul,
            3: self.store,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            9: self.set_relative_base,
            99: self.halt,
        }

    def parse_opcode(self, opcode):
        string_opcode = str(opcode).zfill(self.max_args + 2)
        opcode = int(string_opcode[-2:])
        modes = [int(digit) for digit in string_opcode[:-2]][::-1]
        return opcode, modes

    def add(self, modes):
        # OPCODE 1
        a_i, b_i, c_i = modes[:3]
        a = self.get_arg(self.index + 1, a_i)
        b = self.get_arg(self.index + 2, b_i)
        self.write(self.index + 3, a + b, c_i)
        self.index += 4
        return False

    def mul(self, modes):
        # OPCODE 2
        a_i, b_i, c_i = modes[:3]
        a = self.get_arg(self.index + 1, a_i)
        b = self.get_arg(self.index + 2, b_i)
        self.write(self.index + 3, a * b, c_i)
        self.index += 4
        return False

    def store(self, modes):
        # OPCODE 3
        a_i = modes[0]
        if self.inputs is None:
            input_val = int(input('INPUT: '))
        elif not self.inputs:
            return True
        else:
            input_val = self.inputs.pop(0)
        self.write(self.index + 1, input_val, a_i)
        self.index += 2
        return False


    def output(self, modes):
        # OPCODE 4
        a_i = modes[0]
        a = self.get_arg(self.index + 1, a_i)
        self.outputs.append(a)
        self.index += 2
        return False

    def jump_if_true(self, modes):
        a_i, b_i = modes[:2]
        a = self.get_arg(self.index + 1, a_i)
        b = self.get_arg(self.index + 2, b_i)
        if a == 0:
            self.index += 3
        else:
            self.index = b
        return False

    def jump_if_false(self, modes):
        a_i, b_i = modes[:2]
        a = self.get_arg(self.index + 1, a_i)
        b = self.get_arg(self.index + 2, b_i)
        if a != 0:
            self.index += 3
        else:
            self.index = b
        return False

    def less_than(self, modes):
        a_i, b_i, c_i = modes[:3]
        a = self.get_arg(self.index + 1, a_i)
        b = self.get_arg(self.index + 2, b_i)
        if a < b:
            self.write(self.index + 3, 1, c_i)
        else:
            self.write(self.index + 3, 0, c_i)
        self.index += 4
        return False

    def equals(self, modes):
        a_i, b_i, c_i = modes[:3]
        a = self.get_arg(self.index + 1, a_i)
        b = self.get_arg(self.index + 2, b_i)
        if a == b:
            self.write(self.index + 3, 1, c_i)
        else:
            self.write(self.index + 3, 0, c_i)
        self.index += 4
        return False

    def set_relative_base(self, modes):
        a_i = modes[0]
        a = self.get_arg(self.index + 1, a_i)
        self.relative_base += a
        self.index += 2
        return False

    def halt(self, modes):
        self.index += 1
        self.halted = True
        return True