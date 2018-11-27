from raytrace import *
from tkinter import *

class Test(Frame):
    def __init__(self, master):
        super().__init__()
        self.grid()

        bench = OpticalBench()
        bench.add(Lens(10, 3, 1.5, 1.5, -1.5))
        bench.add(Lens(20, 3, 1.5, 1.5, -1.5))
        bench.add(Lens(30, 3, 1.5, 1.5, -1.5))
        bench.add(Lens(40, 3, 1.5, 1.5, -1.5))
        self.lensframe = LensWidget(self,bench)
        self.lensframe.grid()
#def __init__(self, position, diameter, index, r_left, r_right)

#lens info: pos, diameter, index, r_left, r_right, f, remove button
class LensFrame(Frame):
    def __init__(self, parent, lens, col_width=10):
        # Initialize self as Frame and use grid geometry manager
        super().__init__(parent)
        self.grid()
        
        Label(self, text=format(lens.pos,     '%sg' % col_width)).grid(row=0,column=0,sticky=E)
        Label(self, text=format(lens.diameter,'%sg' % col_width)).grid(row=0,column=1,sticky=E)
        Label(self, text=format(lens.index,   '%sg' % col_width)).grid(row=0,column=2,sticky=E)
        Label(self, text=format(lens.r_left,  '%sg' % col_width)).grid(row=0,column=3,sticky=E)
        Label(self, text=format(lens.r_right, '%sg' % col_width)).grid(row=0,column=4,sticky=E)
        Label(self, text=format(lens.f,       '%sg' % col_width)).grid(row=0,column=5,sticky=E)
        Button(self, text="Remove",command=lambda: parent.remove(lens.pos)).grid(row=0,column=6,sticky=E)


class LensInput(Frame):
    def __init__(self, parent, col_width=10):
        super().__init__(parent)
        self.grid()
        col_width = 12

        self.pos = DoubleVar()
        self.dia = DoubleVar()
        self.ind = DoubleVar()
        self.r_l = DoubleVar()
        self.r_r = DoubleVar()

        self.pos.set(10)
        self.dia.set(10)
        self.ind.set(1.5)
        self.r_l.set(15)
        self.r_r.set(-15)

        Entry(self, textvariable=self.pos,width=col_width).grid(row=0,column=0)
        Entry(self, textvariable=self.dia,width=col_width).grid(row=0,column=1)
        Entry(self, textvariable=self.ind,width=col_width).grid(row=0,column=2)
        Entry(self, textvariable=self.r_l,width=col_width).grid(row=0,column=3)
        Entry(self, textvariable=self.r_r,width=col_width).grid(row=0,column=4)
        Label(self, text=format("",'%ss' % col_width)).grid(row=0,column=5)
        Button(self, text="Add",command=lambda: parent.add(self.get_lens())).grid(row=0,column=6,sticky=E)

    def get_lens(self):
        return Lens(self.pos.get(),self.dia.get(),self.ind.get(),self.r_l.get(),self.r_r.get())

# make a classy looking display from an OpticalBench object.
# Give ability to add and remove lenses as needed
class LensWidget(Frame):
    def __init__(self, parent, bench):
        super().__init__()
        self.grid()
        self.rows = []
        self.col_width = 20
        self.bench = bench

        # Create the header string
        headers = ["Position","Diameter","Index","Left Radius","Right Radius","Focal Length"]
        header = ""
        for item in headers:
            header += format(item, '%ss' % self.col_width)
        Label(self,text=header).grid(row=0,sticky=W)

        LensInput(self,self.col_width).grid(row=2,sticky=W)

        #Grid the rows
        self.update()

    def remove(self,pos):
        self.bench.remove(pos)
        self.update()

    def add(self,lens):
        if self.bench.has(lens.pos):
            pass #add warning message eventually
        else:
            self.bench.add(lens)
            self.update()

    # Clear all gridded rows and replace them with new OpticalBench info
    def update(self):
        for row in self.rows:
            row.grid_remove()
        r = 3
        self.rows = []
        Label(text='').grid(row=0)
        for lens in self.bench.lenses:
            self.rows.append(LensFrame(self,lens,self.col_width))
            self.rows[-1].grid(row=r,sticky=W)
            r+=1

root = Tk()
root.winfo_toplevel().title("Test")
app = Test(root)

root.mainloop()