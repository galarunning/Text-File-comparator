####################################################################################
####################################################################################
####################################################################################
############################# ** MAIN SOURCE CODE ** ###############################
####################################################################################
####################################################################################
####################################################################################
####################################################################################


# Import the libraries to create the gui and navigate the windwos file systems

from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

# Variables to store the data extrapolated from the text files
pre_data = None
post_data = None

# If the files are not calibration files marker
mark = True

# Global arrays to store the results.
res_ZDLY = []
res_Power_pre = []
res_Power_post = []
ZDLY=1
POWER=1

report_directory = ""
name_report = ""

pre_freq = ""
post_freq = ""

###################################### FUNCTIONS ###############################

# Function to define the save menu
def save():

    filetext = ("*"*50)+"REPORT"+("*"*50)+"\n\n\n" + "Generated on {}\n\n".format(datetime.now()) + "CLOG POWER Values(Need to be witin 0 and -5) for PRE-CALIBRATION FILE:\n{}\n\n".format(res_Power_pre) + "ZDLY Values differences (need to be less than 1000): \n{}".format(res_ZDLY)
    f = filedialog.asksaveasfile(initialfile="Report.txt",
    defaultextension=".txt", filetypes=[("AllFiles","*.*"),("Text Document",".txt")])
    if f is None:
        return
    if (res_Power_pre == []) or (res_ZDLY == []):
        messagebox.showwarning(title="Empty Report",message="Either no files were loaded or ZDLY/CLOG values could not be found.")
    f.write(filetext)
    f.close()


# Function to define command for View Pre cal file
def view_precal():

    popup1 = Tk()
    popup1.geometry("600x600")
    popup1.resizable("True","True")

    popup1.title("Pre-Calibration file Preview")
    
    # Always remeber to pack the frame!
    fr = Frame(popup1,bd=1,padx=0,pady=1)
    fr.pack()
    txt = Text(fr,height=600,width=600)
    txt.pack()

    # Getting rid of the /n character
    var = t1.get("1.0",END)
    var = var.strip(var[-1::])
    f = open(var,"r")
    txt.insert(END,f.readlines())
    

#Function to define command for "View Post cal file"
def view_postcal():

    popup1 = Tk()
    popup1.geometry("600x600")
    popup1.resizable("True","True")

    popup1.title("Post-Calibration file Preview")

    # Always remeber to pack your frame!
    fr = Frame(popup1,bd=1,padx=0,pady=1)
    fr.pack()
    txt = Text(fr,height=600,width=600)
    txt.pack()

    # Getting rid of the /n character with strip function
    var = t2.get("1.0",END)
    var = var.strip(var[-1::])
    f = open(var,"r")
    txt.insert(END,f.readlines())
    


# Function to define the About menu
def About():
    messagebox.showinfo(title="Information", message="""Utility version= V0.92\n
Designed for GSS9000/GSS7000 calibrations\n
This calibration text comparator utility was written by Matteo Gala in GS Support.\n
This utility is not been designed to be shared with customers.\n
For more information please contact Matteo at: matteo.gala@spirent.com\n
    """)

def Help():
    messagebox.showinfo(title="How to Use", message= """
To load files you can press the ... button next to the textbox.\n
To compare the files click the Compare Data button and this will give you a visual representation if the tests passed.\n
This utility will compare the differences of the ZDLY values of the two text files (need to be less than 1000).
It also checkes that the CLOG values are between 0 and -5.\n
Within the File submenu you will find the "View pre/post file" buttons. These will allow you to view the files you have loaded in, however will not allow you to modify them.\n
Within the same menu tthe Save As button will allow you to save the report once again in case you want to save it again in another location and are too lazy to click the Save Report button.\n
For more information or to report a bug please send the steps to matteo.gala@spirent.com and I will take a look as soon as possible.
""")


# Function to select the file and read it to get the important values stored
def select_pre_file():

    try:
        t1.delete("1.0",END)
        
        filetypes = (
            ("text files", "*.txt"),
            ("All files", "*.*")
        )

        filename = filedialog.askopenfilename(title="Open a file",
        initialdir=r"C:\Program Files (x86)\Spirent Communications\Auto Calibration Utility\Backup",
        filetypes=filetypes)
        
        # Print the directory in the entry box
        t1.insert(END,filename)

        # Get the file and open it
        pre_cal_dir = filename
        
        f = open(pre_cal_dir,"r")

        # Assigning the data in the text file to a variable as a list
        global pre_data
        pre_data = f.readlines()

        f.close()
    
    except FileNotFoundError:
        messagebox.showerror(title="No File Selected", message="You need to select a file")


# Function to open the post calibration file
def select_post_file():
    
    try:
        t2.delete("1.0",END)
        
        filetypes = (
            ("text files", "*.txt"),
            ("All files", "*.*")
        )

        filename = filedialog.askopenfilename(title="Open a file",
        initialdir=r"C:\Program Files (x86)\Spirent Communications\Auto Calibration Utility\Backup",
        filetypes=filetypes)
        
        # Print the directory in the entry box
        t2.insert(END,filename)

        # Get the file and open it
        pre_cal_dir = filename
        
        f = open(pre_cal_dir,"r")
        global post_data
        post_data = f.readlines()

        f.close()

    except FileNotFoundError:
        messagebox.showerror(title="No File Selected", message="You need to select a file")



# Function to compare the two files loaded
def compare():
    
    # Comparing Serial Numbers of the two files!
    #x = 0

    #Zeroing the results otherwise get appended if you call the function again!
    global res_Power_post 
    global res_Power_pre 
    global res_ZDLY 
    global pre_freq
    global post_freq

    res_Power_post = []
    res_Power_pre = []
    res_ZDLY = []

    # Creating constant to signal if comparison passed or not
    colour_CLOG = "Green"
    colour_ZDLY = "Green"
    c_ZDLY = u'\u2713'
    c_CLOG = u'\u2713'
    global mark

    SN_POST = ""
    SN_PRE = ""

    
    # If empty warn the user there is nothing to compare
    if (pre_data==None) | (post_data==None):
        
        messagebox.showerror(title="One or no files selected",
        message="""Only one or no files have been selected.\n
Please load a file by the ... icon or typing the directory of the file in the white textbox.""")
        
        # Exit the whole function, nothing to compare
        return 0    

      
    if ("Serial Number:" not in pre_data[3]):
        SN_PRE = "NO SN for pre data"
        # print("Pre cal file - no SN at expected index 3 of pre_data list")

    if ("Serial Number:" not in post_data[3]):
        SN_POST = "NO SN for post data"
        # print("Post cal file - no SN at expected index 3 of post_data list")

    # Serial Number check!
    for i in pre_data:
        if "Serial Number" in i:
            SN_PRE = i
        #x += 1
    
    for i in post_data:
        if "Serial Number" in i:
            SN_POST = i
        #x+=1
    
    if SN_POST != SN_PRE:
        messagebox.showwarning(title= "Warning",
        message="Different Serial Numbers detected in the files loaded")
        mark = False

    # Frequencies check
    x = 1
    for i in pre_data:
        if "Frequency"in i:
            pre_freq = i + pre_data[x]
        x+=1
    
    x = 1
    for i in post_data:
        if "Frequency"in i:
            post_freq = i + pre_data[x]
        x+=1

    x = 0
    y = 1

    # Only execute if serial numbers are the same and they are calibration files
    if mark:

        # Delay calibration - Compare the ZDLY values:
        for a,b in zip(pre_data,post_data):

            if ("ZDLY" in a) & ("ZDLY" in b):
                
                # Exit the loop after you checked first 68 lines otherwise an indexError will pop up

                cond_pre = pre_data[x+y].split()[0]
                cond_post = post_data[x+y].split()[0]
                
                try: 
                    while (int(cond_pre)<=500000000) & (int(cond_post)<=5000000000):

                        # Compare the ZDLY values of the two files - Currently NOT working
                        for w,z in zip(pre_data[x+y].split(),post_data[x+y].split()):
                            
                            diff = abs(int(w)-int(z))
                            res_ZDLY.append(diff) # APPENDING RESULTS

                            # If out of tolerance warn user
                            if diff >= 1000:
                                messagebox.showwarning(title="ZDLY values out of Tolerance",
                                message="""It was found that the ZDLY values for pre and 
    post calibration data are out by more than 1000 ps (maximum tolerance).\n
    This will be highlighted in the report.\n
    The index for the value out of tolernace is: {}.\n
    The computed difference between the two files is of {} ({} in the pre calibration data and {} in the post calibration data)
    """.format(y,abs(int(w)-int(z)),w,z))
                                colour_ZDLY = "Red"
                                c_ZDLY = u'\u274C'
                            else:
                                pass
                        
                        y+=1

                        # Update the conditions
                        cond_pre = pre_data[x+y].split()[0]
                        cond_post = post_data[x+y].split()[0]

                except ValueError:
                    messagebox.showwarning(title="Exception",
                    message="""Value Error at index = {}""".format(y))
                    break

                except IndexError:
                    break

            x+=1

        # Now comparing the CLOG Values are within 0 and -5, resetting iterators
        x = 0
        y = 1

        # POWER calibration - check the CLOG Values:
        for a,b in zip(pre_data,post_data):

            if ("CLOG" in a) & ("CLOG" in b):

                # Exit the loop after you checked first 68 lines otherwise an indexError will pop up

                cond_pre = pre_data[x+y].split()[0]
                cond_post = post_data[x+y].split()[0]

                try: 
                    while (float(cond_pre)<1000) & (float(cond_post)<1000):

                        for w,z in zip(pre_data[x+y].split(),post_data[x+y].split()):
                            clog1 = abs(float(w))
                            clog2 = abs(float(z))

                            # If out of tolerance for clog1 warn user
                            if clog1 >= 5:
                                messagebox.showwarning(title="CLOG Value out of Tolerance",
                                message="""A CLOG Value detected is over the boundary of 0 to -5.\n
    it will be shown in the report.\n The recorded value it is of {} at index {}
    """.format(clog1,y))
                                colour_CLOG = "Red"
                                c_CLOG = u'\u274C'

                                res_Power_pre.append("{}".format(clog1))
                                res_Power_post.append("{}".format(clog2))

                            #If out of tolerance for clog2
                            elif clog2 >= 5:
                                messagebox.showwarning(title="CLOG Value out of Tolerance",
                                message="""A CLOG Value detected is over the boundary of 0 to -5.\n
    it will be shown in the report.\n The recorded value it is of {} at index {}
    """.format(clog1,y))
                                colour_CLOG = "Red"
                                c_CLOG = u'\u274C'

                                res_Power_pre.append("{}".format(clog1))
                                res_Power_post.append("{}".format(clog2))

                            else:

                                res_Power_pre.append("{}".format(clog1))
                                res_Power_post.append("{}".format(clog2))

                        y+=1

                        # Update the conditions
                        cond_pre = pre_data[x+y].split()[0]
                        cond_post = post_data[x+y].split()[0]

                except ValueError:
                    messagebox.showwarning(title="Exception",
                    message="""Value Error at index = {}""".format(y))
                    break

                except IndexError:
                    break

            x+=1
            

        # Generate the Report in the GUI!!!
        l3 = Label(frame_3,text="CLOG Values: ")
        l3.grid(row=0,column=0)
        l6 = Label(frame_3,text=c_CLOG,fg=colour_CLOG)
        l6.grid(row=0,column=1,padx=3)
        
        l4 = Label(frame_3,text="ZDLY Values: ")
        l4.grid(row=0,column=3)
        l6 = Label(frame_3,text= c_ZDLY,fg=colour_ZDLY)
        l6.grid(row=0,column=4,padx=3)
        
        

# Function to generate report
def report():

    # Formatting the Frequencies!
    
    # Formatting the CLOG Values - I could do this with multi-dimensional arrays! -Done it by converting data into list and addin \n every 12 numbers
    power_string_pre =""
    x = 1

    for i in res_Power_pre:
        i = "-"+ i + "\t"
        power_string_pre = power_string_pre + f"{i}"
        
        if (x%12 == 0):
            temp = power_string_pre.split("\t")
            temp[x] = "\n"
            power_string_pre = "\t".join(temp)
        x+=1
    
    power_string_post =""
    x = 1

    for i in res_Power_post:
        i = "-"+ i + "\t"
        power_string_post = power_string_post + f"{i}"
        
        if (x%12 == 0):
            temp = power_string_post.split("\t")
            temp[x] = "\n"
            power_string_post = "\t".join(temp)
        x+=1

    # Formatting ZDLY Values for GSS9000 
    
    if (len(power_string_pre.split("\t")) == 121) | (len(power_string_post.split("t")) == 121):
        # print("GSS9000! 10Channel banks detected :)")
        
        # Formatting the ZDLY Values for GSS7000- Creating a string initially --- MASSIVE HEADACHE
        zdly_string = ""
        index = 0
        small_zero = [2,5,14,17,26,29,38,41,50,53,62,65,74,77,86,89,98,101,110,113]
        
        for i in res_ZDLY:
            if index in small_zero:
                zdly_string = zdly_string + "{} ".format(i)
            else: 
                zdly_string = zdly_string +"{:05d} ".format(i)
            index+=1
        
        temp = zdly_string.split(" ")
        
        x = 1
        
        index_tabs = [2,6,16,20,30,34,44,48,58,62,72,76,86,90,100,104,114,118,128,132]
        
        for i in index_tabs:
            temp.insert(i+1,"\t")

        index_newline = [14,29,44,59,74,89,104,119,134,149]
        
        for i in index_newline:
            temp.insert(i,"\n")
        temp.insert(0," ")
        zdly_string = " ".join(temp)
        
        # Eliminate the first white space
        index = [0]
        for i in index:
            zdly_string = ""+zdly_string[i+1:]
    
    elif (len(power_string_pre.split("\t")) == 49) | (len(power_string_post.split("\t")) == 49):

        # Formatting the ZDLY Values for GSS7000- Creating a string initially --- MASSIVE HEADACHE
        zdly_string = ""
        
        index_tabs = [2,6,9,17,21,24,32,36,39,47,51,54]
        index = 0
        small_zero = [2,5,7,14,17,19,26,29,31,38,41,43]
        for i in res_ZDLY:
            if index in small_zero:
                zdly_string = zdly_string + "{} ".format(i)
            else:
                zdly_string = zdly_string + "{:05d} ".format(i)
            index += 1
        
        temp = zdly_string.split(" ")
        x = 1
        
        for i in index_tabs:
            temp.insert(i+1,"\t")

        index_newline = [15,31,47]
        for i in index_newline:
            temp.insert(i,"\n")
        temp.insert(0," ")
        zdly_string = " ".join(temp)
        
        # Eliminate the first white space
        index = [0]
        for i in index:
            zdly_string = ""+zdly_string[i+1:]

    else:
        messagebox.showerror(title="Did not recognise number of channel banks",message="""
This utility is coded to use either 10 channel banks (GSS9000) or 4 channel banks (GSS7000).
In this case a different number was detected.\n\n{}""".format(len(power_string_pre.split("\t"))))
        return

        
    # Getting title of files compared from the Text box
    file1 = t1.get(1.0,END)
    file2 = t2.get(1.0,END)

    # Getting Date and time in correct format to save file
    datetitle = f"{datetime.now()}"
    datetitle = datetitle.replace(":","-")
    datetitle = datetitle.replace(".","-")
    
    # Store string in a variable and pass it in when saving the file
    astrics = ("*"*50)
    separator = ("-"*120)
    filetext = f"""{astrics} REPORT {astrics}\n\n\n
Generated on {datetime.now()}\n\n\n{separator}
This Report has been generated by comparing the following files:\n\n
1. {file1}\n2. {file2}\n\n\n{separator}
{pre_freq}\n\n{separator}
CLOG POWER Values(Need to be within 0 and -5):\n\n
PRE-CALIBRATION FILE:\n\n{power_string_pre}\n\n
POST-CALIBRATION FILE:\n\n{power_string_post}\n\n
{separator}
ZDLY Values differences (need to be less than 1000):\n\n{zdly_string}"""
    global name_report 
    name_report = "Report {}.txt".format(datetitle)
    f = filedialog.asksaveasfile(initialfile=name_report,
    defaultextension=".txt", filetypes=[("AllFiles","*.*"),("Text Document",".txt")])
    name_report = f.name

    # Not making it crash if no files were selected to generate report
    if f is None:
        return
    f.write(filetext)
    
    f.close()

# Function to View the report that you have created.

def view_report():
    
    popup1 = Tk()
    popup1.geometry("600x600")
    popup1.resizable("True","True")

    popup1.title("Report file preview")

    fr = Frame(popup1,bd=1,padx=0,pady=1)
    fr.pack()
    txt = Text(fr,height=600,width=600)
    txt.pack()
    try:
        with open(name_report,"r") as f:
            text = f.readlines()
            txt.insert(END,text)
    except FileNotFoundError:
        txt.insert(END,"A problem occurred trying to find your report.")



############################################################################
############################## GUI #########################################
############################################################################

# Start the design of the window
window = Tk()

# Geometry of the window
window.geometry("600x325")
window.resizable("True","True")

# Title
window.title("Calibration Files Comparator V0.92")

# Distributing the frames(containers)
frame_logo = LabelFrame(window,bd=0,padx=0,pady=0)
frame_logo.pack(anchor="n",padx=0,pady=0)
frame_1 = LabelFrame(window,text="Pre-calibration data",padx=10,pady=7)
frame_1.pack(anchor="n",padx=5,pady=5)
frame_2 = LabelFrame(window,text="Post calibration Data",padx=10,pady=7)
frame_2.pack(anchor="n",padx=5,pady=5)
frame_3 = LabelFrame(window,padx=5,pady=5,bd=1)
frame_3.pack(anchor="n",side="top",pady=15)
frame_4 = LabelFrame(window,text="",padx=2,pady=2)
frame_4.pack(anchor="n",side="top")
# frame_5 = LabelFrame(window,text="")
# frame_5.pack(anchor="n",side="top",pady=15)

# Define the top menu
mainmenu = Menu(window)
window.config(menu=mainmenu)

# Start adding the options by creating cascade options for File
file_menu = Menu(mainmenu,tearoff=False)
mainmenu.add_cascade(label="File",menu=file_menu)
# file_menu.add_command(label="New...",command=New_file)
file_menu.add_command(label="View Pre-calibration file",command=view_precal)
file_menu.add_command(label="View Post-calibration file",command=view_postcal)
file_menu.add_command(label="Save Roprt as", command=save)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=window.quit)

# Creating an Help menu for Version etc.
mainmenu.add_command(label="About",command=About)
mainmenu.add_command(label="Help",command=Help)
window.config(menu=mainmenu)

# Importing a Spirent image
# pic = PhotoImage(file=r"C:/files/download.png")
# l1 = Label(frame_logo,image=pic)#,background="Blue")
# l1.pack()

# Importing the Spirent logo instead of the TKinter default logo (can't make it work)
# window.iconbitmap(r"C:/files/unamed.ico")

# MAIN WINDOW DESIGN - Labels and entry boxes

# Entry 1 + Button
v1 = StringVar(frame_1,value="")
t1 = Text(frame_1,height=1,width=65)
t1.grid(row=0,column=0)

l_dots1 = Button(frame_1, text="...", command=select_pre_file)
l_dots1.grid(row=0, column=1,padx=4)
B_viewpost = Button(frame_1,text="View Pre Calibration File",command=view_precal)
B_viewpost.grid(row=1,column=0)

# Entry 2 + Button
v2 = StringVar(frame_2,value="")
t2 = Text(frame_2,height=1,width=65)
t2.grid(row=0,column=0)

l_dots2 = Button(frame_2, text="...", command=select_post_file)
l_dots2.grid(row=0, column=1,padx=4)
B_viewpost = Button(frame_2,text="View Post Calibration File",command=view_postcal)
B_viewpost.grid(row=1,column=0)

# Analyse data Button
b1 = Button(frame_3,text="Compare Data",command=compare,bd=2)
b1.grid(row=0,column=2)

# Generate Report Button
b2 = Button(frame_4,text="Generate Report",command=report,bd=2)
b2.grid(row=0,column=0)

# Place line in between
l1 = Canvas(frame_4, width=2, height=10)
l1.grid(row=0,column=1)
# l1.create_line(163,10,163,0, fill="gray", width=2,)

# View Report Button
b3 = Button(frame_4,text="View Report",command=view_report,bd=2,padx=10)
b3.grid(row=0,column=2)

# Main Infinite loop for main GUI
window.mainloop()




