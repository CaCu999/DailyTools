import tkinter as tk

class EventLisnter:
    def __init__(self, app:tk.Tk):
        self.app = app
        self._progress:dict[object, tk.IntVar] = {}
        self._btns:dict[object, tk.Button] = {}
    
    def add_progress(self, pro:tk.IntVar, event):
        self._progress[event] = pro
    
    def add_btn(self, btn:tk.Button, event):
        self._btns[event] = btn
    
    def deal_progress(self, event, val:int):
        def update_ui():
            if self._progress.get(event):
                self._progress[event].set(val) if val <= 100 else self._progress[event].set(100)
        self.app.after(0, update_ui)
    
    def deal_complete(self, event):
        def update_ui():
            if self._btns.get(event):
                self._btns[event].config(state='active')
        self.app.after(0, update_ui)

class ProgressPublisher:
    def __init__(self):
        self._listener:list[EventLisnter] = []

    def add_listener(self, listener:EventLisnter):
        self._listener.append(listener)

    def on_progress(self, index: int, total:int, other:str = ""):
        self.terminal_process(index, total, other)
        # print(len(self._listener))
        for l in self._listener:
            l.deal_progress(self, int((index) * 100 / total))
        if index >= total:
            self.on_complete()
    
    def terminal_process(self, index:int, total:int, other:str = ""):    
        filled = (index) * 100 // total
        precent = (index) * 100 / total
        bar = '=' * filled + '>' + '.' * (100-filled-1)
        print(f'\r[{bar}]{precent:.1f}% {index}/{total} {other}', end='')
    
    def on_complete(self):
        for l in self._listener:
            l.deal_complete(self)

if __name__ == "__main__":
    pass