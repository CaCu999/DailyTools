import tkinter as tk
from LocalTranslator import LocalTransor
import threading
import keyboard

def setText(text:tk.Text, content):
    text.delete('1.0', 'end')
    content = str(content)
    text.insert('end', content)
    
class TraslatorWindow:
    def ensure(self):
        th = threading.Thread(target=self.translate, daemon=True)
        th.start()

    def translate(self):
        input = self.inputVar.get('1.0','end')
        res = self.translator.translate(input)
        setText(self.outputVar, res)

    def show_window(self):
        input = self.window.clipboard_get()
        input = input.replace('\r\n', '\n').replace('\r','\n')
        setText(self.inputVar, input)
        self.window.deiconify()
        self.window.attributes('-topmost', True)
        self.window.focus_force()
        self.window.after(500, lambda: self.window.attributes('-topmost', False))
        self.translate()

    def __init__(self):
        self.translator = LocalTransor()
        self.window = tk.Tk()
        self.window.geometry("300x800")
        frame1 = tk.Frame(self.window)
        label1 = tk.Label(frame1, text="input")
        label1.place(relx=0.01, rely=0.01, relheight=0.05, relwidth=0.15)
        self.inputVar = tk.Text(frame1)
        self.inputVar.place(relx=0.01, rely=0.08, relheight=0.9, relwidth=0.98)

        frame2 = tk.Frame(self.window)
        label2 = tk.Label(frame2, text="output:")
        label2.place(relx=0.01, rely=0.01, relheight=0.1, relwidth=0.15)
        btn = tk.Button(frame2, text="translate", command=self.ensure)
        btn.place(relx=0.75, rely=0.01, relwidth=0.2, relheight=0.1)
        self.outputVar = tk.Text(frame2)
        self.outputVar.place(relx=0.01, rely=0.11, relheight=0.88, relwidth=0.98)

        frame1.place(relx=0, rely=0, relheight=0.5, relwidth=1)
        frame2.place(relx=0, rely=0.5, relheight=0.5, relwidth=1)

        # self.window.bind('<Control-Alt-c>', self.show_window)

    def register_hotkeys(self):
        keyboard.add_hotkey('ctrl+shift+c', self.show_window)

    def start_keyboard_listener(self):
        def listener():
            try:
                keyboard.wait()
            except KeyboardInterrupt:
                setText(self.outputVar, "key board error.")
        listener_thread = threading.Thread(target=listener, daemon=True)
        listener_thread.start()

    def run(self):
        self.register_hotkeys()
        self.start_keyboard_listener()
        self.window.mainloop()

if __name__ == "__main__" :
    window = TraslatorWindow()
    window.run()