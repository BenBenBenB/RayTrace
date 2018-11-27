# The graphical portion of the Ray Trace program 1
# Made by Ben Burton for Dr. Eric Klumpe for PHYS 3520

from raytrace import *
from tkinter import *

class inputVariableWidget:

    def __init__(self, master):

    	# Create the whole frame to be added
        frame = Frame(master)
        frame.grid()

        self.bench = OpticalBench()

        self.source_input = SourceWidget(frame)
        self.source_input.grid(row=0,column=0,sticky=N)
        self.lens_input = LensWidget(frame,self.bench)
        self.lens_input.grid(row=0,column=2,sticky=N)
 
        # the button to button all buttons
        b = Button(frame,
                    text="Generate Graph",
                    command=self.gen_graph).grid(row=5,sticky=N)

	# the function to generate a graph, used for button
    def gen_graph(self):
        if len(self.bench.lenses) == 0:
            return False
        plt.clf()
        #trace =RayTrace(app.num_rays.get(),bench.lenses,alpha=app.alpha.get())
        if self.source_input.v.get() == 1: # Point Source
            trace = RayTrace(self.source_input.num_rays.get(),
                             self.bench.lenses,
                             z_init=self.source_input.z_init.get(),
                             x_init=self.source_input.x_init.get())
        else: # Collimated Source
            trace = RayTrace(self.source_input.num_rays.get(),
                             self.bench.lenses,
                             alpha=self.source_input.alpha.get())     
        # Spit out some numbers:

        #Show the Plot:
        plt.show()       

class SourceWidget(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid()

        # Create the variables
        self.alpha = DoubleVar()
        self.num_rays = IntVar()
        self.z_init = DoubleVar()
        self.x_init = DoubleVar()

        # Initilize the variables
        self.alpha.set(1)
        self.num_rays.set(3)
        self.z_init.set(0.5)
        self.x_init.set(0)

        EntryWidget(self, self.num_rays,"Number of Rays:").grid(row=0,sticky=W)


        radio_frame = Frame(self)
        radio_frame.grid()
        self.v = IntVar()
        self.v.set(1)
        Label(radio_frame, text="Source Type:").grid(row=1,sticky = W)
        Radiobutton(radio_frame, 
                      text="Point Source",
                      padx = 10, 
                      variable=self.v,
                      command=lambda:self.update_inputs(),
                      value=1).grid(row=1,sticky=W)
        Radiobutton(radio_frame, 
                      text="Collimated Source",
                      padx = 10, 
                      variable=self.v, 
                      command=lambda:self.update_inputs(),
                      value=2).grid(row=1,column=1,sticky=W)



        self.e1 = EntryWidget(self, self.z_init,"Initial z:")
        self.e2 = EntryWidget(self, self.x_init,"Initial x:")
        self.e3 = EntryWidget(self, self.alpha,"Incident angle:","°")
        
        self.e1.grid(row=2,sticky=W)
        self.e2.grid(row=3,sticky=W)
        self.e3.grid_forget()

    def update_inputs(self):

        if (self.v.get() == 1): #Point source
            self.e3.grid_forget()

            self.e1.grid(row=2,sticky=W)
            self.e2.grid(row=3,sticky=W)

        else: # v == 2, Collimated Source
            self.e1.grid_forget()
            self.e2.grid_forget()

            self.e3.grid(row=2,sticky=W)


# A simple entry field: [prelabel][Field][postlabel]
class EntryWidget(Frame):
    def __init__(self, parent, variable, prelabel='', postlabel=''):
        super().__init__(parent)
        self.grid()
        self.prelabel = Label(self, text=prelabel).grid(row=0,column=0,sticky=E)
        self.entry = Entry(self, textvariable=variable).grid(row=0,column=1,sticky=E)
        self.postlabel= Label(self, text=postlabel).grid(row=0,column=2,sticky=W)



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
root.winfo_toplevel().title("Ray Tracer")
app = inputVariableWidget(root)

root.mainloop()