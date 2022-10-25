from time import time
from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor
from dialog import Dialog
from mainwindow import Mainwindow
from InputDialog import InputDialog

class TreeDemo(Mainwindow):
    def __init__(self):
        super().__init__()
        # set window's title.
        self.title('Tree Demo')
        # set window's geometry size
        self.geometry('600x400')

        self.item_menu = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.item_menu, label='Item', underline= 0)

        # Add Menu Items
        self.item_menu.add_command(label='Insert Item', command=self.insert_item)
        self.item_menu.add_command(label='Insert Subitem', command=self.insert_subitem)
        self.item_menu.add_separator()
        self.item_menu.add_command(label='Remove Item', command=self.remove_item)
        self.item_menu.add_command(label='Remove All', command=self.remove_all)
        self.item_menu.add_command(label='Modify Item', command=self.modify_item)
        # self.item_menu.add_separator()
        # self.item_menu.add_command(label='Move Up', command=self.move_up)
        # self.item_menu.add_command(label='Move Down', command=self.move_down)

        # column_name : (heading, width, anchor)
        cols = {
            'A' : ('A', 50, CENTER),
            'B' : ('B', 50, E),
            'C' : ('C', 50, W)
        }

        self.tree = ttk.Treeview(self.mainframe, columns=tuple(cols.keys()))
        for k in cols:
            self.tree.heading(k, text=cols[k][0])
            self.tree.column(k, width=cols[k][1], anchor=cols[k][2])
        self.tree.grid(column=0, row=0, sticky=NSEW)

        self.tree.bind('<Double-1>', func=self.tree_select)
        self.entry = None

        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(0, weight=1)

        self.values = [1,10,100]

        self.showmessage('Ready.')

    def insert_item(self):
        self.values = [v + 1 for v in self.values]
        focus_item = self.tree.focus()
        self.showmessage(focus_item)
        if focus_item == '':
            self.tree.insert('', 'end', text='', values=self.values)    
        else:
            self.tree.insert(self.tree.parent(focus_item), 'end', text=str(time()), values=self.values)    

    def insert_subitem(self):
        self.values = [v + 1 for v in self.values]
        self.tree.insert(self.tree.focus(), 'end', text='', values=self.values)        

    def remove_item(self):
        self.tree.delete(self.tree.focus())

    def remove_all(self):
        top_items = self.tree.get_children()
        for item in top_items:
            self.tree.delete(item)

    def modify_item(self):
        focus_item = self.tree.focus()
        if focus_item != '':
            self.values = [v + 1 for v in self.values]
            for i, v in enumerate(self.values):
                self.tree.set(focus_item, i, v)

    def tree_select(self, e: Event):
        item = self.tree.selection()[0]
        # print(item, ':', self.tree.bbox(item))

        for i, col in enumerate(self.tree['columns']):
            x, y, w, h =  self.tree.bbox(item, col)
            if x < e.x < x + w and y < e.y < y + h:
                print(x, y, w, h)
                text = self.tree.item(item, 'values')[i]
                dlg = InputDialog(self, 'Set Value', text=text)
                dlg.show()
                self.tree.set(item, col, dlg.var.get())
                break
        else:
            # click text area
            text = self.tree.item(item, 'text')
            dlg = InputDialog(self, 'Set Value', text=text)
            dlg.show()
            self.tree.item(item, text=dlg.var.get())


if __name__ == '__main__':
    mw = TreeDemo()
    mw.mainloop()