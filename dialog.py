"""
Modal Dialog class.

Copyright (c) 2022 falwat<falwat@163.com>, under MIT licence.
"""
from tkinter import *

class Dialog(Toplevel):
    def __init__(self, master=None, **kw) -> None:
        super().__init__(master, **kw)
        self.protocol("WM_DELETE_WINDOW", self.destroy) # intercept close button
        self.transient(master)   # dialog window is related to main
        self.wait_visibility() # can't grab until window appears, so we wait
        self.grab_set()        # ensure all input goes to our window
        # place dialog below parent if running htest
        self.geometry("+%d+%d" % (
                        master.winfo_rootx()+30,
                        master.winfo_rooty()+30))

    def destroy(self):
        self.grab_release()
        super().destroy()

    def show(self):
        self.wait_window()

if __name__ == '__main__':
    from tkinter import ttk
    from mainwindow import Mainwindow

    # This is a example.
    class DemoDialog(Dialog):
        def __init__(self, master=None, title = '', text = '', **kw) -> None:
            super().__init__(master, **kw)
            self.textVar = StringVar(value=text)
            self.entry = ttk.Entry(self, textvariable=self.textVar)
            self.entry.grid(column=0, row=0, sticky=NSEW)
            # self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.title(title)
            self.geometry('400x25')

        def destroy(self):
            print('good bye')
            return super().destroy()

    class DemoWindow(Mainwindow):
        """
        Demo window inherited from Mainwindow.
        """
        def __init__(self):
            super().__init__()
            # set window's title.
            self.title('Demo')
            # set window's geometry size
            self.geometry('600x400')
            self.showmessage('Ready.')
            ttk.Button(self.mainframe, text='show dialog', command=self.show_dialog).grid(row=0, column=0)

        def show_dialog(self):
            dialog = DemoDialog(self, title='Input Your Name', text='Jackie Wang')
            dialog.show()
            print(dialog.textVar.get())

    mw = DemoWindow()
    mw.mainloop()