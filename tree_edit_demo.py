from InputDialog import InputDialog
from mainwindow import Mainwindow
from tkinter import *
from tkinter import ttk

class Demo(Mainwindow):
    """
    Demo window inherited from Mainwindow.
    """
    def __init__(self):
        super().__init__()
        # set window's title.
        self.title('Demo')
        # set window's geometry size
        self.geometry('600x400')
        self.tree = ttk.Treeview(self.mainframe)
        self.tree.grid(column=0, row=0, sticky=NSEW)
        self.tree.bind('<Double-1>', func=self.tree_item_edit)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(0,weight=1)
        self.init_tree()
        self.delegate_var = StringVar()
        self.showmessage('Ready.')
    def init_tree(self):
        self.cols = {
            # 'name': ('Attribute Name', 100, W),
            'name': ('Name', 100, W),
            'age': ('Age', 100, W),
            'gender': ('Gender', 100, W),
        }
        self.tree['columns'] = tuple(self.cols.keys())
        for k, v in self.cols.items():
            self.tree.column(k, width=v[1], anchor=v[2])
            self.tree.heading(k, text=v[0])

        self.items = {}
        self.items['name'] = self.tree.insert('', 'end', text='1001', values=('Ada', '18','female'))
        self.items['name'] = self.tree.insert('', 'end', text='1002', values=('bob', '19','male'))
        self.items['name'] = self.tree.insert('', 'end', text='1003', values=('jack', '22','male'))

    def tree_item_edit(self, e: Event):
        self.selected_item = self.tree.selection()[0]

        for i, col in enumerate(self.tree['columns']):
            x, y, w, h =  self.tree.bbox(self.selected_item, col)
            if x < e.x < x + w and y < e.y < y + h:
                print(w)
                self.selected_column = col
                text = self.tree.item(self.selected_item, 'values')[i]
                break
        else:
            # click text area
            self.selected_column = None
            x, y, w, h =  self.tree.bbox(self.selected_item)
            text = self.tree.item(self.selected_item, 'text')

        self.delegate_var.set(text)
        if self.selected_column == 'gender':
            self.delegate_widget = ttk.Combobox(self.tree, width=w // 8, textvariable=self.delegate_var, values=('male', 'female'))
            self.delegate_widget.bind('<<ComboboxSelected>>', self.tree_item_edit_done)
            self.delegate_widget.bind('<FocusOut>', func=self.tree_item_edit_done)
        elif self.selected_column == 'age':
            self.delegate_widget = ttk.Spinbox(self.tree, width=w // 8, textvariable=self.delegate_var, from_=1, to=100)
            self.delegate_widget.bind('<FocusOut>', func=self.tree_item_edit_done)
        else:
            self.delegate_widget = ttk.Entry(self.tree, width=w // 8, textvariable=self.delegate_var)
            self.delegate_widget.bind('<FocusOut>', func=self.tree_item_edit_done)

        self.delegate_widget.grid(padx=x, pady=y)
        self.delegate_widget.focus()

    def tree_item_edit_done(self, e):
        self.delegate_widget.grid_forget()
        if self.selected_column is None:
            self.tree.item(self.selected_item, text=self.delegate_var.get())
        else:
            self.tree.set(self.selected_item, self.selected_column, self.delegate_var.get())

if __name__ == '__main__':
    mw = Demo()
    mw.mainloop()