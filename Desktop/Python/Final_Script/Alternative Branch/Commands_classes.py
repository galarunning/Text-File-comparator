from socket import inet_aton
from os import chdir
from tkinter import Label,messagebox,END 
import subprocess
from sys import stdout
import datetime


#region IP_settings
# Class that contains only the commands to write IP addresses 

class IP_Commands:

    def __init__(self,master,gui):

        self.gui = gui
        self.master = master
    
    # Function to Write the IP address of the simulator
    def ip_windows(self):

        self.gui.IP_windows = self.gui.windows_ip.get()
        # Check that the IP adress is valid
        try:
            # Method from socket module
            inet_aton(self.gui.IP_windows)
            path = "IP_GSS_Win.txt"
            self.f = open(path,"w+")
            self.f.write(self.gui.IP_windows)
            self.f.close()
            self.gui.l_win = Label(self.gui.frame3,font="Ariel 18",text=u'\u2713',
                        fg="Green")
            self.gui.l_win.grid(row=0,column=2)
            self.gui.windows_ip.config(state="readonly")

        except OSError:
            self.gui.l_win = Label(self.gui.frame3,font="Ariel 18",text=u'\u274C',
                        fg="Red")
            self.gui.l_win.grid(row=0,column=2)  
            messagebox.showerror(title="IP adress not valid", 
                                message= f"""The entered IP power adress is {self.gui.IP_windows}\n
This is not valid! It should be in the format of nnn.nnn.nnn.nnn without spaces and with the points.""")
   
    ##### Functions to write IP address of Power switch into text file #####
    def ip_powerswitch(self):
        
        # Calling this definition again to update it
        self.gui.IP_Power = self.gui.power_ip.get() 

        # Check that the IP adress is valid
        try:
            #Method from socket module
            inet_aton(self.gui.IP_Power)
            path = "IP_Power.txt"
            self.gui.f = open(path,"w+")
            self.gui.f.write(self.gui.IP_Power)
            self.gui.f.close()
            self.gui.l_power = Label(self.gui.frame2,font="Ariel 18",text=u'\u2713',
                        fg="Green")
            self.gui.l_power.grid(row=0,column=2)
            self.gui.power_ip.config(state="readonly")

        except OSError:

            self.gui.l_power = Label(self.gui.frame2,font="Ariel 18",text=u'\u274C',
                        fg="Red")
            self.gui.l_power.grid(row=0,column=2)
            messagebox.showerror(title="IP adress not valid", 
                                message= f"""The entered IP power adress is {self.gui.IP_Power}\n
This is not valid! It should be in the format of 0-255.0-255.0-255.0-255 without spaces and with the points.""")
#endregion IP_settings


#region stop_scripts
class Stop_powercycles:

    def __init__(self,master,gui):

        self.gui = gui
        self.master = master
    
    def stop_infinitescript(self):

        self.gui.stop_powershell = True
        
        ################ Resetting ALL the entry widget to editable
        self.gui.infinite_button.config(state="normal")
        self.gui.num_powercycles.config(state="normal")
        self.gui.windows_ip.config(state="normal")
        self.gui.power_ip.config(state="normal")
        self.gui.set_button.config(background='SystemButtonFace')

        ############## Clearing the entries 
        self.gui.windows_ip.delete(0,END)
        self.gui.power_ip.delete(0,END)
        self.gui.num_powercycles.delete(0,END)

        ############### Now deleting the checkmark on IP addresses entry bars
        try:    
            self.gui.l_power.grid_forget()
        except AttributeError:
            # Print a line for debug purposes only as this is not an error!
            print("l_power was not found, cannot hide it")

        try:    
            self.gui.l_win.grid_forget()
        except AttributeError:
            # Print a line for debug purposes only as this is not an error!
            print("l_win was not found, cannot hide it")

        print(f"The script has done: {self.gui.loops} amount of total power cycles")
        print("The powershell script will be stopped from being called")
        print("However, it needs to finish its current cycle, so do not be surprised if it looks like is still going.")

#endregion stop_scripts


#region reboot script

class Boot_script:

    def __init__(self,gui,master):
        self.gui = gui
        self.master = master

    # Function to run Powershell script
    def powershell_scripts(self):

        ############## Implemented the powershell script to run from same dir of EXE
        ############## Tested
        # Ensuring I set thisvariable to False so I can start calling the scripts
        
        self.gui.stop_powershell = False
        
        # Ensuring the loop variable is set back to 0
        self.gui.loops = 0
        
        seconds_for_powershell_script = 200

        # Printing the chosen power swtich port so the user knows.
        print(f"Starting Powershell Script!\nSelected Power switch port number: {self.gui.selected_power.get()}")

        if self.gui.selected_power.get() == "Port 1":
            for x in range(0,self.gui.num_of_powercycles_intvar.get()):
                if self.gui.stop_powershell == False:
                    try:
                        time1 = (datetime.datetime.now())
                        chdir("C:\\Program Files (x86)\Automatic boot utility")   
                        subprocess.call(["powershell", ".\Script_Power_1.ps1"], stdout=stdout)
                        time2 = (datetime.datetime.now())
                        time_diff = time2-time1
                    except:
                        time1 = (datetime.datetime.now())
                        subprocess.call(["powershell", ".\Script_Power_1.ps1"], stdout=stdout)
                        time2 = (datetime.datetime.now())
                        time_diff = time2 - time1

                    # Printing total seconds that the powershell script has been running for
                    print(f"Total Time for this powercycle: {time_diff.total_seconds()}")

                    if time_diff.total_seconds()>seconds_for_powershell_script:
                        self.gui.loops +=1

        elif self.gui.selected_power.get() == "Port 2":
            for x in range(0,self.gui.num_of_powercycles_intvar.get()):
                if self.gui.stop_powershell == False:
                    try:
                        time1 = (datetime.datetime.now())
                        chdir("C:\\Program Files (x86)\Automatic boot utility")   
                        subprocess.call(["powershell", ".\Script_Power_2.ps1"], stdout=stdout)
                        time2 = (datetime.datetime.now())
                        time_diff = time2-time1
                    except:
                        time1 = (datetime.datetime.now())
                        subprocess.call(["powershell", ".\Script_Power_2.ps1"], stdout=stdout)
                        time2 = (datetime.datetime.now())
                        time_diff = time2 - time1

                    # Printing total seconds that the powershell script has been running for
                    print(f"Total Time for this powercycle: {time_diff.total_seconds()}")

                    if time_diff.total_seconds()>seconds_for_powershell_script:
                        self.gui.loops +=1
                    
        elif self.gui.selected_power.get() == "Port 3":
            for x in range(0,self.gui.num_of_powercycles_intvar.get()):
               if self.gui.stop_powershell == False:
                    try:
                        time1 = (datetime.datetime.now())
                        chdir("C:\\Program Files (x86)\Automatic boot utility")   
                        subprocess.call(["powershell", ".\Script_Power_3.ps1"], stdout=stdout)
                        time2 = (datetime.datetime.now())
                        time_diff = time2-time1
                    except:
                        time1 = (datetime.datetime.now())
                        subprocess.call(["powershell", ".\Script_Power_3.ps1"], stdout=stdout)
                        time2 = (datetime.datetime.now())
                        time_diff = time2 - time1

                    # Printing total seconds that the powershell script has been running for
                    print(f"Total Time for this powercycle: {time_diff.total_seconds()}")

                    if time_diff.total_seconds()>seconds_for_powershell_script:
                        self.gui.loops +=1

        elif self.gui.selected_power.get() == "Port 4":
            for x in range(0,self.gui.num_of_powercycles_intvar.get()):
                if self.gui.stop_powershell == False:
                    try:
                        time1 = (datetime.datetime.now())
                        chdir("C:\\Program Files (x86)\Automatic boot utility")   
                        subprocess.call(["powershell", ".\Script_Power_4.ps1"], stdout=stdout)
                        time2 = (datetime.datetime.now())
                        time_diff = time2-time1
                    except:
                        time1 = (datetime.datetime.now())
                        subprocess.call(["powershell", ".\Script_Power_4.ps1"], stdout=stdout)
                        time2 = (datetime.datetime.now())
                        time_diff = time2 - time1

                    # Printing total seconds that the powershell script has been running for
                    print(f"Total Time for this powercycle: {time_diff.total_seconds()}")

                    if time_diff.total_seconds()>seconds_for_powershell_script:
                        self.gui.loops +=1

        else:
            messagebox.showerror(title="No power switch port selected",
            message="""Please select a power switch from the dropdown.\n
Otherwise the utility does not know which unit to power off.""")
            return
        
        print("**************** Reboots completed: ",self.gui.loops," ***************")

#endregion reboot script


#region Set nu. Powercycles

class Set_powercycles:

    def __init__(self,gui,master):
        self.gui = gui
        self.master = master
    
    def set_powercycles(self):
        
        if self.gui.set_button.cget("background") == "Green":

            self.gui.set_button.configure(background='SystemButtonFace')
            self.gui.num_powercycles.config(state="normal")

        else:
            
            # Give user feedback that the number has been set
            self.gui.set_button.config(background="Green")
            self.gui.num_powercycles.config(state="readonly")

        return

    # Inifinite Powershell Call
    def infinite_powershellcall(self):

        # If the entry text of num of powercycles is readonly and it has the infinite simbol
        
        if (self.gui.num_powercycles.get() == '\u221e') & (self.gui.num_powercycles.cget("state") == "readonly"):
            
            self.gui.num_powercycles.config(state="normal")
            self.gui.num_powercycles.delete(0,END)

        else:

            self.gui.num_powercycles.delete(0,END)
            self.gui.num_powercycles.insert(0,'\u221e')
            print(f"Number of powercycles I will attempt are almost infinite!")
            
            self.gui.num_of_powercycles_intvar = 1000000000000
            # To add the ability to read only the amount of powercycles
            self.gui.num_powercycles.config(state="readonly")

#endregion


#region report

class Report:
     
    def __init__(self,gui,master):
        self.gui = gui
        self.master = master

    def generate_report(self):
        
        self.gui.f = open(r"results.txt", "w+")
        self.gui.f.write("The number of successfull reboots were:{}".format(self.loops))
        self.gui.f.write("---------------------------------------------")
        self.gui.f.write("\n\n\n\nThe time of the last event is:")
        self.gui.f.write("".format(datetime.datetime.now()))
        self.gui.f.close()


#endregion