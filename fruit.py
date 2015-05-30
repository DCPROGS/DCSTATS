from Tkinter import Tk, Frame, Label, Entry, StringVar

class fruitlist:
    def entryupdate(self, sv, i):
        print(sv, i, self.fruit[i], sv.get())
    
    def __init__(self, root):
        cf = Frame(root)
        cf.pack()
        self.sva = []
        self.fruit = ("Apple", "Banana", "Cherry", "Date")
        for f in self.fruit:
            i = len(self.sva)
            self.sva.append(StringVar())
            self.sva[i].trace("w", lambda name, index, mode, var=self.sva[i], i=i:
                              self.entryupdate(var, i))
            Label(cf, text=f).grid(column=2, row=i)
            Entry(cf, width=6, textvariable=self.sva[i]).grid(column=4, row=i)

root = Tk()
root.title("EntryUpdate")
app = fruitlist(root)
root.mainloop() 
