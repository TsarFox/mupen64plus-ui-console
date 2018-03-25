import readline
import shutil

import llm64p


COLORS = {
    "none": "0m",
    "red": "31;1m",
    "green": "32;1m",
}


def _ansi_wrap(text: str, code: str):
    return "\x1b[{}{}\x1b[0m".format(code, text)


def printc(*args, **kwargs):
    code = "none"
    if "color" in kwargs:
        code = COLORS.get(kwargs.get("color"), "none")
        del kwargs["color"]
    return print(_ansi_wrap(" ".join(args), code), **kwargs)


class Display:
    def __init__(self):
        self.last_regs = []

    def draw_header(self, name):
        width, _ = shutil.get_terminal_size((80, 20))
        rpad = width - len(name) - len("[  ]") - 4

        printc("----[ ", end="", color="green")
        printc(name, end="", color="red")
        printc(" ]" + "-" * rpad, end="", color="green")
        print()

    def draw_regs(self):
        ["r0",
         "at",
         "v0", "v1",
         "a0", "a1", "a2", "a3",
         "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
         "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",
         "t8", "t9",
         "k0", "k1",
         "gp",
         "sp",
         "sB",
         "ra"]

        columns = []
        row = []

        for reg in ["pc", "sp", "ra", "gp", "at", "sB"]:
            row.append((reg, llm64p.get_reg(reg)))

        columns.append(row)
        row = []

        for reg in ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9"]:
            row.append((reg, llm64p.get_reg(reg)))

        columns.append(row)
        row = []

        for reg in ["a0", "a1", "a2", "a3"]:
            row.append((reg, llm64p.get_reg(reg)))

        columns.append(row)
        row = []

        for reg in ["v0", "v1"]:
            row.append((reg, llm64p.get_reg(reg)))

        columns.append(row)
        row = []

        for reg in ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7"]:
            row.append((reg, llm64p.get_reg(reg)))

        columns.append(row)

        # self.last_regs = regs


        for i in range(10):
            for column in columns:
                if i < len(column):
                    reg, val = column[i]
                    line = "{}: {}".format(reg, hex(val)).ljust(18)

                    # if column[i] in changed:
                    #     print(gefred(line), end="")
                    # else:
                    #     print(line, end="")
                    print(line, end="")
                else:
                    print("".ljust(18), end="")
            print()

    def draw(self):
        self.draw_header("regs")
        self.draw_regs()


disp = Display()
while True:
    disp.draw()
    eval(input(">>> "))
