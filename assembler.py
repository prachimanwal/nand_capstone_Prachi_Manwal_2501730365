import os
import sys

# Predefined symbols in Hack assembly
SYMBOLS = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7,
    "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
    "SCREEN": 16384, "KBD": 24576
}

COMP_TABLE = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "A+D": "0000010",
    "D-A": "0010011", "A-D": "0000111", "D&A": "0000000", "A&D": "0000000",
    "D|A": "0010101", "A|D": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "M+D": "1000010", "D-M": "1010011",
    "M-D": "1000111", "D&M": "1000000", "M&D": "1000000", "D|M": "1010101", "M|D": "1010101"
}

DEST_TABLE = {
    "": "000", "M": "001", "D": "010", "MD": "011", "DM": "011",
    "A": "100", "AM": "101", "MA": "101", "AD": "110", "DA": "110",
    "AMD": "111", "ADM": "111"
}

JUMP_TABLE = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}


def clean_line(line):
    if "//" in line:
        line = line[:line.index("//")]
    return line.strip().replace(" ", "").replace("\t", "")


def assemble(filename):
    with open(filename, "r") as f:
        raw_lines = f.readlines()

    symbol_table = dict(SYMBOLS)
    seen_labels = {}
    instructions = []
    rom_addr = 0

    # First pass: remove comments/blank lines and find labels
    # Extra feature for K = 65 (65 mod 3 = 2): print warning if same label is written twice
    for line_no, raw in enumerate(raw_lines, start=1):
        line = clean_line(raw)
        if not line:
            continue

        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            if label in seen_labels:
                print(f"Warning: label '{label}' written twice at line {line_no}")
            else:
                symbol_table[label] = rom_addr
                seen_labels[label] = rom_addr
        else:
            instructions.append((line_no, line))
            rom_addr += 1

    # Second pass: convert instructions to 16-bit binary
    next_ram = 16
    output_lines = []

    for line_no, inst in instructions:
        if inst.startswith("@"):
            val = inst[1:]
            if val.isdigit():
                addr = int(val)
            else:
                if val not in symbol_table:
                    symbol_table[val] = next_ram
                    next_ram += 1
                addr = symbol_table[val]
            output_lines.append(format(addr, "016b"))
        else:
            dest = ""
            comp = inst
            jump = ""

            if "=" in comp:
                dest, comp = comp.split("=", 1)
            if ";" in comp:
                comp, jump = comp.split(";", 1)

            if comp not in COMP_TABLE or dest not in DEST_TABLE or jump not in JUMP_TABLE:
                print(f"Line {line_no}: invalid instruction {inst}")
                sys.exit(1)

            binary = "111" + COMP_TABLE[comp] + DEST_TABLE[dest] + JUMP_TABLE[jump]
            output_lines.append(binary)

    out_file = os.path.splitext(filename)[0] + ".hack"
    with open(out_file, "w") as f:
        for b in output_lines:
            f.write(b + "\n")

    print(f"Created {out_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <file.asm>")
        sys.exit(1)
    for arg in sys.argv[1:]:
        assemble(arg)
