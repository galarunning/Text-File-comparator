
##########################################################
# An attempt to re-build the whole application using OOP #
##########################################################

# For this program to run the powershell scripts must be placed
# in the C:\\Program Files (x86)\Automatic boot utility directory.power switch to sel

from tkinter import ttk, Tk
from tkinter import messagebox,Label,Frame,LabelFrame,Button, Entry
from tkinter import StringVar, IntVar, BOTH
from threading import Thread
import Commands_classes

# Setting up the skeleton
root = Tk()
root.geometry("400x350")
root.title("GSS Reboot Controller V0.3")


class GUI:

    # Constructor which is all the Graphical
    def __init__(self, master):
        
        #Setting some important variables
        self.selected_power = StringVar()
        self.loops = 0
        self.num_of_powercycles_intvar = IntVar()

        # Setting up a boolean in case the powershell wants to be stopped.
        # This boolean is modified in the stop function
        
        self.stop_powershell = False

        #region objects to get the commands

        self.Report = Commands_classes.Report(gui=self,master=master)
        self.Set_Powercycles = Commands_classes.Set_powercycles(gui=self,master=master)
        self.IP_Commands = Commands_classes.IP_Commands(master=master,gui=self)
        self.powercycles = Commands_classes.Boot_script(gui=self,master=master)
        self.stop_powercycles = Commands_classes.Stop_powercycles(
            master=master, gui=self)
        #endregion

        #region Frames

        # Frame for start button
        self.frame1 = Frame(root,padx=0,pady=5)

        self.frame1.pack(side="bottom",padx=5,pady=5)

        self.frame2 = LabelFrame(root,
                            text="IP Address of Power Switch",
                            padx=5,pady=5)
        self.frame2.pack(side = "top",padx=5,pady=5)

        self.frame3 = LabelFrame(root,
                            text="IP Adress of Simulator",
                            padx=5, pady=5)
        self.frame3.pack(side="top")

        self.frame4 = LabelFrame(root,
                            text="Power Switch port to select",
                            padx=5,pady=5)
        self.frame4.pack(side="top",padx=5,pady=5)

        # Entry Box to get number of powercycles
        self.frame5 = Frame(root)
        self.frame5.pack(side="top",padx=5, pady=5)

        ##### Last frame for the Terminal #####
        self.frame6 = Frame(root)
        self.frame6.pack(fill=BOTH, expand=True)

        #endregion Frames

        #region start and stop button
        
        # Start button
        self.start = Button(self.frame1,text="Start",
                    background="Green",
                    font="Ariel 12",
                    # Using Thread which is a class from the threading module
                    command=lambda: Thread(
                            target=self.powercycles.powershell_scripts).start())
        self.start.grid(column=0,row=1,padx=10)

        ######### Stop button #######
        self.stop = Button(self.frame1,text="Stop",
                    font="Ariel 12",background="Red",
                    command=self.stop_powercycles.stop_infinitescript)
        self.stop.grid(column=2,row=1,padx=10)

        #endregion start/stop button
        
        # region report button
        # Generate report button
        self.Report = Button(self.frame1,text="Generate Report",
                        font="Ariel 12",command=self.Report.generate_report)
        self.Report.grid(column=1,row=1,padx=10)
        
        #endregion

        # region IP addresses buttons
        ##### Importing class giving commands for writing IP addresses
        
        ###### Entry box for the IP Address of the Power Switch
        self.power_ip = Entry(self.frame2,width=20,font="Ariel 18")
        self.power_ip.grid(row=0,column=0,padx=5,pady=5)

        self.power_ip_set = Button(self.frame2,text="Set",
                            font="Ariel 12",
                            command=self.IP_Commands.ip_powerswitch)
        self.power_ip_set.grid(row=0,column=1,padx=5,pady=5)

        ###### Entry box for the IP adress of the Windows side
        self.windows_ip = Entry(self.frame3,width=20,font="Ariel 18")
        self.windows_ip.grid(row=0,column=0,padx=5,pady=5)

        self.windows_ip_set = Button(self.frame3,text="Set",
                                font="Ariel 12",
                                command=self.IP_Commands.ip_windows)
        self.windows_ip_set.grid(row=0,column=1,padx=5,pady=5)

        #endregion

        #region ComboBox for controlling which powershell script to call #################

        # Defining Tuple of variable options that will give the desired options
        self.switches = ("Port 1", "Port 2", "Port 3", "Port 4")

        # Defining the combobox that will have the self.selected_power textvariable global variable
        self.Switch_selected = ttk.Combobox(self.frame4,width=20,font="Ariel 18",textvariable=self.selected_power,state="readonly")

        # Inserting the values in the Combobox
        self.Switch_selected["values"] = self.switches

        # Implementing logic to call the correct port to turn off
        self.Switch_selected.grid(row=0,column=0,padx=5,pady=5)

        #endregion

        self.iteration_number = Label(self.frame5,text="Desired number of powercycles: ")
        self.iteration_number.grid(row=0, column=0)

        self.num_powercycles = Entry(self.frame5,width= 4,font="Ariel 18",textvariable=self.num_of_powercycles_intvar,state="normal")
        self.num_powercycles.grid(row=0,column=1)

        self.infinite_button = Button(self.frame5,text='\u221e', font="Calibri 12",command=self.Set_Powercycles.infinite_powershellcall)
        self.infinite_button.grid(row=0, column=2, padx=2)

        self.set_button = Button(self.frame5, text="Set", font="Calibri 12",command=self.Set_Powercycles.set_powercycles)
        self.set_button.grid(row=0, column=3, padx=1)

#Creating an instance of the GUI Class
GUI(root)

# Entering the infinite loop :) 
root.mainloop()

