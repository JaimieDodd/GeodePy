from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import geodepy.transform as tf


class MainScreen:
    def __init__(self, master):

        # sets defaults for some variables
        self.outheader = IntVar()
        self.headerout = 0
        self.master = master

        # Sets up the main screen
        self.master.title("GeodePy Transformation")
        self.master.iconname("GeodePy")

        self.label = Label(master, text="Select .CSV Files:")
        self.label.grid(row=0, column=0, columnspan=10, sticky=W)

        # Input file button
        self.infile_button = Button(master, text="Select Input File", command=self.infile)
        self.infile_button.grid(row=3, column=0, sticky=W)
        self.inlabel = Label(master, textvariable="")
        self.inlabel.grid(row=3, column=1, sticky=W)

        # Output file button, file location label & header checkbox
        self.outfile_button = Button(master, text="Select Output File", command=self.outfile)
        self.outfile_button.grid(row=4, column=0, sticky=W)
        self.outlabel = Label(master, textvariable="")
        self.outlabel.grid(row=4, column=1, columnspan=2, sticky=W)

        self.outheader_label = Label(master, text="Do you want to write a header in the output file?")
        self.outheader_label.grid(row=5, column=0, sticky=W)
        self.outheader_cbutton = Checkbutton(master, text="Yes", variable = self.outheader, command=self.outheadcb)
        self.outheader_cbutton.grid(row=5,column=2, sticky=W)


        #Creates the Notebook
        self.nb = ttk.Notebook(root)
        self.nb.grid(row=7, column=0, columnspan=50, rowspan=49, sticky='NESW')

        #Adds the GeotoGrid Frame to the notebook
        geotogridtab = ttk.Frame(self.nb)
        self.nb.add(geotogridtab, text="Geographic to Grid")

        #Adds the GridtoGeo Frame to the notebook
        gridtogeotab = ttk.Frame(self.nb)
        self.nb.add(gridtogeotab, text="Grid to Geographic")

        ###
        # Sets out the GeotoGrid Tab
        self.geocsv_label = Label(geotogridtab,
                                        text="Input Format of CSV: Point ID, Latitude, Longitude")
        self.geocsv_label.grid(row=2, column=0)
        self.geotype_label = Label(geotogridtab,
                                        text="Latitude and Longitude Format")
        self.geotype_label.grid(row=3, column=0)

        # Lat and Long format Radio buttons
        self.geotypein = StringVar()
        self.geotypein.set("DD")
        self.rb1DD = Radiobutton(geotogridtab, text="Decimal Degrees", variable=self.geotypein, value="DD")
        self.rb1DD.grid(row=4, column=0)
        self.rb1DMS = Radiobutton(geotogridtab, text="Degrees Minutes Seconds", variable=self.geotypein, value="DMS")
        self.rb1DMS.grid(row=4, column=1)
        #self.rb1HP = Radiobutton(geotogridtab, text="HP (DDD.MMSSSS)", variable=self.geotypein, value="HP")
        #self.rb1HP.grid(row=4,column=2)


        self.GeotoGrid_button = Button(geotogridtab, text="Convert", command=self.GeotoGrid)
        self.GeotoGrid_button.grid(row=5)

        ###
        # Sets out the GridtoGeo Tab
        self.gridinheader_label = Label(gridtogeotab,
                                        text="Input Format: Point ID, UTM Zone, Easting (m), Northing (m)")
        self.gridinheader_label.grid(row=2, column=0)
        self.geoouttype_label = Label(gridtogeotab,
                                        text="Output Latitude and Longitude Format")
        self.geoouttype_label.grid(row=3, column=0)

        # Lat and Long format Radio buttons
        self.geotypeout = StringVar()
        self.geotypeout.set("DD")
        self.rb2DD = Radiobutton(gridtogeotab, text="Decimal Degrees", variable=self.geotypeout, value="DD")
        self.rb2DD.grid(row=4, column=0)
        self.rb2DMS = Radiobutton(gridtogeotab, text="Degrees Minutes Seconds", variable=self.geotypeout, value="DMS")
        self.rb2DMS.grid(row=4, column=1)
        #self.rb2HP = Radiobutton(gridtogeotab, text="HP (DDD.MMSSSS)", variable=self.geotypeout, value="HP")
        #self.rb2HP.grid(row=4,column=2)

        self.GridtoGeo_button = Button(gridtogeotab, text="Convert", command=self.GridtoGeo)
        self.GridtoGeo_button.grid(row=7, column=0)


    def infile(self):
        root.infilename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("CSV", "*.csv"), ("all files", "*.*")))
        self.fn = root.infilename
        self.inlabel.config(text=self.fn)

    def outfile(self):
        root.outfilename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                         filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        self.fn_out = root.outfilename + ".csv"
        self.outlabel.config(text=self.fn_out)


    def outheadcb(self):
        self.headerout = self.outheader.get()


    def GeotoGrid(self):
        tf.geo2gridio(self.fn, self.fn_out, self.headerout, self.geotypein)

    def GridtoGeo(self):
        tf.grid2geoio(self.fn, self.fn_out, self.headerout, self.geotypeout)



root = Tk()
my_gui = MainScreen(root)
root.mainloop()





