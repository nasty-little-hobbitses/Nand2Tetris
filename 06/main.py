#MACROS
COMMENT_ = -2
A_CMD = 0
C_CMD = 1
LABEL_ = 2


class SymbolTable:
    def __init__(self, file_path):
        self.file_path = file_path

        self.table = { #symbol reference table
                'SP':0, 
                'LCL':1, 
                'ARG':2, 
                'THIS':3, 
                'THAT':4,
                'R0':0, 
                'R1':1, 
                'R2':2, 
                'R3':3, 
                'R4':4, 
                'R5':5, 
                'R6':6, 
                'R7':7,
                'R8':8, 
                'R9':9, 
                'R10':10, 
                'R11':11, 
                'R12':12, 
                'R13':13, 
                'R14':14, 
                'R15':15,
                'SCREEN':16384, 
                'KBD':24576
        }

        for i in range(16): #variables are stored in RAM[16] and further
            self.table[f"R{i}"] = i

    def AddEntry(self, symbol, value):
        self.table[symbol] = value

    def first_pass(self): #first pass is translating without symbols
        parser = Parser(self.file_path)
        parser.start_parsing()

        while True:
            command = parser.next_command()
            if command.type == -1: #end of file
                break
            elif command.type == LABEL_:
                self.AddEntry(command.symbol, command.line)


class Command:
    def __init__(self):
        self.type = None
        self.line = 0
        self.symbol = None
        self.dest_bit_seq = None
        self.comp_bit_seq = None
        self.jump_bit_seq = None


class Parser: #checking for different kinds of commands
    def __init__(self, ip_file):
        self.ip_file = ip_file
        self._file_handle = None
        self.current_line = -1 #end of file

    def start_parsing(self):
        self._file_handle = open(self.ip_file, 'r')

    def next_command(self):
        command_str = self._file_handle.readline()

        command = Command()
        if not command_str:
            self._file_handle.close()
            command.type = -1 #end of file
            return command

        command_str = command_str.strip()
        if not command_str or command_str.startswith("//"): #if symbolic command starts with //, it's a command
            command.type = COMMENT_
            return command

        if "//" in command_str:
            command_str = command_str.split("//")[0]

        self.current_line += 1

        first_char = command_str[0]

        if first_char == "@": #if symbolic command starts with @ e.g: @100
            command.type = A_CMD
            command.symbol = command_str[1:]

        elif first_char == "(": #if symbolic command is a label declaration e.g: (LOOP)
            command.type = LABEL_
            command.symbol = command_str[1:-1]
            command.line = self.current_line
            self.current_line -= 1

        else:
            command.type = C_CMD #C command: dest = comp; jump_bit_seq. We omit '=' if dest is empty, and ';' if jump_bit_seq is empty 
            if "=" not in command_str:
                if ";" not in command_str:
                    command.comp_bit_seq = command_str
                else:
                    command.comp_bit_seq, command.jump_bit_seq = list(map(str.strip, command_str.split(";")))
            else:
                if ";" not in command_str:
                    command.dest_bit_seq, command.comp_bit_seq = list(map(str.strip, command_str.split("=")))
                else:
                    dest, comp_jump = command_str.split("=")
                    comp, jump_bit_seq = comp_jump.split(";")
                    command.dest_bit_seq = dest.strip()
                    command.comp_bit_seq = comp.strip()
                    command.jump_bit_seq = jump_bit_seq.strip()

        return command


class Decoder:
    def __init__(self):
        self.COMP_TABLE = { #reference table to convert computation bits to it's corresponding binary value
            "0": "101010",
            "1": "111111",
            "-1": "111010",
            "D": "001100",
            "A": "110000",
            "!D": "001101",
            "!A": "110001",
            "-D": "001111",
            "-A": "110011",
            "D+1": "011111",
            "A+1": "110111",
            "D-1": "001110",
            "A-1": "110010",
            "D+A": "000010",
            "D-A": "010011",
            "A-D": "000111",
            "D&A": "000000",
            "D|A": "010101"
        }

        self.DEST_TABLE = { #reference table to convert destination bits to it's corresponding binary value
            None: bin(0)[2:],
            "M": bin(1)[2:],
            "D": bin(2)[2:],
            "MD": bin(3)[2:],
            "A": bin(4)[2:],
            "AM": bin(5)[2:],
            "AD": bin(6)[2:],
            "AMD": bin(7)[2:],
        }

        self.JMP_TABLE = { #reference table to convert jump command bits to it's corresponding binary value
            None: bin(0)[2:],
            "JGT": bin(1)[2:],
            "JEQ": bin(2)[2:],
            "JGE": bin(3)[2:],
            "JLT": bin(4)[2:],
            "JNE": bin(5)[2:],
            "JLE": bin(6)[2:],
            "JMP": bin(7)[2:],
        }

    def comp_bit_seq(self, comp_bit_seq):
        if comp_bit_seq in self.COMP_TABLE:
            bits = self.COMP_TABLE[comp_bit_seq]
        else:
            bits = self.COMP_TABLE[comp_bit_seq.replace("M", "A")]
        return bits

    def dest_bit_seq(self, dest_bit_seq):
        bits = self.DEST_TABLE[dest_bit_seq]
        padding = "0"*(3 - len(str(bits))) #there are only 3 destination bits 

        destination_string = f"{padding}{bits}"
        return destination_string

    def jump_bit_seq(self, jump_bit_seq):
        bits = self.JMP_TABLE[jump_bit_seq]
        padding = "0" * (3 - len(str(bits))) #there are only 3 jump bits 

        jump_string = f"{padding}{bits}"
        return jump_string