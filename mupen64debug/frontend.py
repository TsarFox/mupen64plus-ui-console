import llm64p
import urwid

KEYSTROKE_TREE = {
    # Initial terminals
    "enter": "eval",
    "backspace": "delete-backward-char",
    "ctrl h": "help",
    "ctrl e": "end-of-line",
    "ctrl a": "beginning-of-line",
    "ctrl n": "forward-hist",
    "ctrl p": "backward-hist",
    "ctrl f": "forward-char",
    "ctrl b": "backward-char",

    # Complex keystrokes
    "ctrl x": {
        "ctrl x": "exit-debugger",
    }
}


def collapse_keystrokes(keystrokes):
    cur = KEYSTROKE_TREE
    for keystroke in keystrokes:
        cur = cur.get(keystroke, None)
        if cur is None:
            return None
        if isinstance(cur, str):
            return cur
    return "incomplete"


class ConsolePrompt(urwid.Edit):
    def __init__(self):
        self.keystrokes = []

        self.prompt = "(m64d) "
        super().__init__(self.prompt)

    def selectable(self):
        return True

    def keypress(self, size, key):
        if len(key) == 1:
            super().keypress(size, key)            
        else:
            self.keystrokes.append(key)
            res = collapse_keystrokes(self.keystrokes)

            if res != "incomplete":
                self.keystrokes = []

            if res == "forward-char":
                self.set_edit_pos(self.edit_pos + 1)

            elif res == "backward-char":
                self.set_edit_pos(self.edit_pos - 1)

            elif res == "end-of-line":
                self.set_edit_pos(len(self.get_edit_text()))

            elif res == "beginning-of-line":
                self.set_edit_pos(0)

            elif res == "delete-backward-char":
                text = self.get_edit_text()
                text = text[:self.edit_pos - 1] + text[self.edit_pos:]
                self.set_edit_text(text)

                if self.edit_pos != len(text):
                    self.set_edit_pos(self.edit_pos - 1)

            elif res == "exit-debugger":
                raise urwid.ExitMainLoop
            elif res == "eval":
                self.try_eval(self.get_edit_text())

    def try_eval(self, line):
        if line == "meme":
            self.set_edit_text("hi")


instructions = urwid.Text("\n".join(
    [" ".join(llm64p.disas_word(llm64p.read_word(addr), addr)) for addr in range(llm64p.get_reg("pc"), llm64p.get_reg("pc") + 0x20, 0x4)]
))


b = urwid.Text("Registers")
awrap = urwid.LineBox(instructions, "Code")
bwrap = urwid.LineBox(b, "Registers")
cols = urwid.Columns([awrap, bwrap])

# prompt = urwid.Edit(">>> ")
prompt = ConsolePrompt()

toplevel = urwid.Pile([cols, prompt])

fill = urwid.Filler(toplevel, "top")
loop = urwid.MainLoop(fill)
loop.run()
