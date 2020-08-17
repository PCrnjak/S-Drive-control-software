# -*- coding: utf-8 -*-
"""
Created on 17.8.2020

@author: Petar Crnjak mm
@Version: 2.0
@Supported S-Drive firmware versions: 3.0
@Supported S-Drive BLDC drivers: V3.2

"""




from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
#import matplotlib.patches as mpatches
from PIL import Image, ImageTk
import tkinter as tk
import numpy as np
import serial as sr
import webbrowser
import time

#link variables
url_donate = 'https://paypal.me/PCrnjak?locale.x=en_US'
url_project = 'https://hackaday.io/project/168324-sdrive-small-bldc-driver'
url_help = 'https://forum.blestron.com'
url_forum = 'https://forum.blestron.com'
url_github = 'https://github.com/PCrnjak/S-Drive-control-software'
url_user_guide = 'https://github.com/PCrnjak/S-Drive-control-software/wiki'

#------global variables

version_txt = "Version: 2.0"

data = {}
data[0] = np.array([])
data[1] = np.array([])
data[2] = np.array([])
data[3] = np.array([])
data[4] = np.array([])
data[5] = np.array([])

Modes = [
    ("Go to position and hold",1),
    ("Speed and signal when at setpoint",2),
    ("Gravity compensation",3),
    ("Strong position hold",4),
    ("Speed and direction",5),
    ("Jump to position",6),
    ("Voltage mode",7)
]


cond = False
cond_start = False
mode_variable = 1
connect_cond = False
cntr = 0

#Serial information if you dont want to type it in Baudrate and COM port fields
s = sr.Serial()
s.baudrate = 2000000
s.port = 'COM5'

root = tk.Tk()
root.title('S-Drive control software')
#root.iconbitmap('F:\\Google Drive\\python_gui\\logo_2.ico')
root.configure(background = "ghostwhite")
# define window geometry and disable minimization
root.geometry("1300x650") 
root.resizable(0,0)

# Function to read out serial data and then plot it
# Data is saved in list of 200 variables and then just shifted 
# when new data comes

#https://stackoverflow.com/questions/55424957/indexerror-list-index-out-of-range-python-arduino

def plot_data():
    global cond, data , cntr, cond_start

    if(cond_start == False and cond == True):
        
        z = s.readline()
        c = '#\n'
        c = c.encode("utf-8")
        if(z == c):
            cond_start = True


    if (cond == True and cond_start == True):
        #https://stackoverflow.com/questions/44356435/remove-first-n-elements-of-bytes-object-without-copying
        a = s.readline()
        #print(type(a))
        a = bytearray(a)
        del a[0] # remove char 't' that is at the beggining of data stream
        a = bytes(a)
        print(a)
        #startTime = time.time()
        x = a.split(b',')
        #x.decode('latin-1')
        if len(x) == 6:
            position_var = x[0].decode("utf-8")
            current_var = x[1].decode("utf-8")
            speed_var = x[2].decode("utf-8")
            temp_var = x[3].decode("utf-8")
            supply_var = x[4].decode("utf-8")
            bemf1_var = x[5].decode("utf-8")

        #startTime = time.time()
        if(cntr == 5):
            info1= tk.Label(root, text="Supply voltage:\n"+str(x[4].decode()) + " mV" \
                "\nTemp:\n"+str(x[3].decode()) + "deg" + "\nSpeed:\n" + str(x[2].decode()) + "RPM" + "\nCurrent:\n"+str(x[1].decode()) \
                    + " mA" +"\nPosition:\n"+str(x[0].decode()) +"\nError:\n"+str(x[5].decode())  ,justify=tk.LEFT ,font = "Verdana 10 ")
            info1.place(x = 10, y = 278)
            cntr = 0

        if(len(data[0]) < 200):
            data[0] = np.append(data[0],int(position_var))
        else:
            data[0][0:199] = data[0][1:200]
            data[0][199] = int(position_var)

        if(len(data[1]) < 200):
            data[1] = np.append(data[1],int(current_var))
        else:
            data[1][0:199] = data[1][1:200]
            data[1][199] = int(current_var)   

        if(len(data[2]) < 200):
            data[2] = np.append(data[2],int(speed_var))
        else:
            data[2][0:199] = data[2][1:200]
            data[2][199] = int(speed_var)

        if(len(data[3]) < 200):
            data[3] = np.append(data[3],int(temp_var))
        else:
            data[3][0:199] = data[3][1:200]
            data[3][199] = int(temp_var)  

        if(len(data[4]) < 200):
            data[4] = np.append(data[4],int(supply_var))
        else:
            data[4][0:199] = data[4][1:200]
            data[4][199] = int(supply_var)      

        if(len(data[5]) < 200):
            data[5] = np.append(data[5],int(bemf1_var))
        else:
            data[5][0:199] = data[5][1:200]
            data[5][199] = int(bemf1_var)


        startTime = time.time()
    
        if(mode_variable == 1):
            if int(position_var) > 0:
                ax.set_ylim(0,int(position_var) + 500)
            elif int(position_var) < 0:
                ax.set_ylim(int(position_var) - 500,0)
            lines[0].set_xdata(np.arange(0,len(data[0])))
            lines[0].set_ydata(data[0])
            canvas.draw()

        elif(mode_variable == 2):
            lines[1].set_xdata(np.arange(0,len(data[1])))
            lines[1].set_ydata(data[1])
            canvas.draw()

        elif(mode_variable == 3):
            lines[2].set_xdata(np.arange(0,len(data[2])))
            lines[2].set_ydata(data[2])
            canvas.draw()

        elif(mode_variable == 4):
            lines[3].set_xdata(np.arange(0,len(data[3])))
            lines[3].set_ydata(data[3])
            canvas.draw()      
   
        elif(mode_variable == 5):
            lines[4].set_xdata(np.arange(0,len(data[4])))
            lines[4].set_ydata(data[4])
            canvas.draw()

        elif(mode_variable == 6):
            lines[5].set_xdata(np.arange(0,len(data[5])))
            lines[5].set_ydata(data[5])
            canvas.draw()    

        elif(mode_variable == 7):
            startTime = time.time()
            lines[0].set_xdata(np.arange(0,len(data[0])))
            lines[0].set_ydata(data[0])
            lines[1].set_xdata(np.arange(0,len(data[1])))
            lines[1].set_ydata(data[1])
            lines[2].set_xdata(np.arange(0,len(data[2])))
            lines[2].set_ydata(data[2])
            canvas.draw()

        new_time = time.time()
        elapsed_time = new_time - startTime
        #print(elapsed_time)
        cntr = cntr + 1
    root.after(1,plot_data)

# Start ploting data
def plot_start():
    global cond
    cond = True
    s.open()
    s.reset_input_buffer()

    if(s.is_open == True):
        status2_l = tk.Label(root, text="Connected" , font = "Verdana 10 ", fg = "green")
        status2_l.place(x = 70, y = 200)
        cond = True
        connect_cond = True
        s.write(b'b')
        s.write(b'\n')
        print("b in plot_start")

    else:
        status2_l = tk.Label(root, text="Connected" , font = "Verdana 10 ", fg = "red")
        status2_l.place(x = 70, y = 200)
        cond = False
        connect_cond = False


# This function creates control panel menu options on right side of the screen 

def control_panel_menu():
    var = v.get()
    global option_positon, option_speed, option_Kp, option_direction, option_Compliance_speed, option_current_tresh, option_voltage 
    global e_position, e_speed, e_Kp, e_current_tresh, e_direction, e_comp_speed, Send_b, e_voltage

    option_positon.destroy()
    option_speed.destroy()
    option_Kp.destroy()
    option_current_tresh.destroy()
    option_direction.destroy()
    option_Compliance_speed.destroy()
    option_voltage.destroy()
    Send_b.destroy()

    e_position.destroy()
    e_speed.destroy()
    e_Kp.destroy()
    e_current_tresh.destroy()
    e_direction.destroy()
    e_comp_speed.destroy()
    e_voltage.destroy()

    if var == 1:

        option_positon = tk.Label(root, text="Positon" , font = "Verdana 9 ")
        option_speed = tk.Label(root, text="Speed" , font = "Verdana 9 ")
        option_Kp = tk.Label(root, text="Kp" , font = "Verdana 9 ")
        option_current_tresh = tk.Label(root, text="Current treshold" , font = "Verdana 9 ")
        
        e_position = tk.Entry(root,width = 15, borderwidth = 2)
        e_speed = tk.Entry(root,width = 15, borderwidth = 2)
        e_Kp = tk.Entry(root,width = 15, borderwidth = 2)
        e_current_tresh = tk.Entry(root,width = 10, borderwidth = 2)

        option_positon.place(x = 1110, y = 370)
        e_position.place(x = 1190, y = 370)
        option_Kp.place(x = 1110, y = 390)
        e_Kp.place(x = 1190, y = 390)
        option_current_tresh.place(x = 1110, y = 410)
        e_current_tresh.place(x = 1220, y = 410)
        option_speed.place(x = 1110, y = 430)
        e_speed.place(x = 1190, y = 430)
        Send_b = tk.Button(root, text = "Send", font = ('calbiri',12), activebackground = "green", width = 15 , command = lambda: write_data())
        Send_b.place(x = 1130, y = 460)
    

    elif var == 2:

        option_positon = tk.Label(root, text="Positon" , font = "Verdana 9 ")
        option_speed = tk.Label(root, text="Speed" , font = "Verdana 9 ")

        e_position = tk.Entry(root,width = 15, borderwidth = 2)
        e_speed = tk.Entry(root,width = 15, borderwidth = 2)
 
        option_positon.place(x = 1110, y = 370)
        e_position.place(x = 1190, y = 370)
        option_speed.place(x = 1110, y = 390)
        e_speed.place(x = 1190, y = 390)
        Send_b = tk.Button(root, text = "Send", font = ('calbiri',12), activebackground = "green", width = 15 , command = lambda: write_data())
        Send_b.place(x = 1130, y = 410)

 
    elif var == 3:

        option_current_tresh = tk.Label(root, text="Current treshold" , font = "Verdana 9 ")
        option_Compliance_speed = tk.Label(root, text="Compliance speed" , font = "Verdana 9 ")

        e_current_tresh = tk.Entry(root,width = 10, borderwidth = 2)
        e_comp_speed = tk.Entry(root,width = 15, borderwidth = 2)

        option_current_tresh.place(x = 1110, y = 370)
        e_current_tresh.place(x = 1220, y = 370)
        option_Compliance_speed.place(x = 1110, y = 390)
        e_comp_speed.place(x = 1190, y = 390)
        Send_b = tk.Button(root, text = "Send", font = ('calbiri',12), activebackground = "green", width = 15 , command = lambda: write_data())
        Send_b.place(x = 1130, y = 410)

 
    elif var == 4:

        option_Kp = tk.Label(root, text="Kp" , font = "Verdana 9 ")
        option_current_tresh = tk.Label(root, text="Current treshold" , font = "Verdana 9 ")

        e_Kp = tk.Entry(root,width = 15, borderwidth = 2)
        e_current_tresh = tk.Entry(root,width = 10, borderwidth = 2)

        option_current_tresh.place(x = 1110, y = 370)
        e_current_tresh.place(x = 1220, y = 370)
        option_Kp.place(x = 1110, y = 390)
        e_Kp.place(x = 1190, y = 390)
        Send_b = tk.Button(root, text = "Send", font = ('calbiri',12), activebackground = "green", width = 15 , command = lambda: write_data())
        Send_b.place(x = 1130, y = 410)

    elif var == 5:

        option_speed = tk.Label(root, text="Speed" , font = "Verdana 9 ")
        option_direction = tk.Label(root, text="Direction" , font = "Verdana 9 ")

        e_speed = tk.Entry(root,width = 15, borderwidth = 2)
        e_direction = tk.Entry(root,width = 15, borderwidth = 2)

        option_direction.place(x = 1110, y = 370)
        e_direction.place(x = 1190, y = 370)
        option_speed.place(x = 1110, y = 390)
        e_speed.place(x = 1190, y = 390)
        Send_b = tk.Button(root, text = "Send", font = ('calbiri',12), activebackground = "green", width = 15 , command = lambda: write_data())
        Send_b.place(x = 1130, y = 410)

    elif var == 6:
        option_positon = tk.Label(root, text="Positon" , font = "Verdana 9 ")
        #option_speed = tk.Label(root, text="Speed" , font = "Verdana 9 ")
        option_Kp = tk.Label(root, text="Kp" , font = "Verdana 9 ")
        option_current_tresh = tk.Label(root, text="Current treshold" , font = "Verdana 9 ")
        
        e_position = tk.Entry(root,width = 15, borderwidth = 2)
        #e_speed = tk.Entry(root,width = 15, borderwidth = 2)
        e_Kp = tk.Entry(root,width = 15, borderwidth = 2)
        e_current_tresh = tk.Entry(root,width = 10, borderwidth = 2)

        option_positon.place(x = 1110, y = 370)
        e_position.place(x = 1190, y = 370)
        option_Kp.place(x = 1110, y = 390)
        e_Kp.place(x = 1190, y = 390)
        option_current_tresh.place(x = 1110, y = 410)
        e_current_tresh.place(x = 1220, y = 410)
        #option_speed.place(x = 1110, y = 430)
        #e_speed.place(x = 1190, y = 430)
        Send_b = tk.Button(root, text = "Send", font = ('calbiri',12), activebackground = "green", width = 15 , command = lambda: write_data())
        Send_b.place(x = 1130, y = 460)

    elif var == 7:

        option_voltage = tk.Label(root, text="Voltage" , font = "Verdana 9 ")
        option_direction = tk.Label(root, text="Direction" , font = "Verdana 9 ")

        e_voltage = tk.Entry(root,width = 15, borderwidth = 2)
        e_direction = tk.Entry(root,width = 15, borderwidth = 2)

        option_direction.place(x = 1110, y = 370)
        e_direction.place(x = 1190, y = 370)
        option_voltage.place(x = 1110, y = 390)
        e_voltage.place(x = 1190, y = 390)
        Send_b = tk.Button(root, text = "Send", font = ('calbiri',12), activebackground = "green", width = 15 , command = lambda: write_data())
        Send_b.place(x = 1130, y = 410)



# https://stackoverflow.com/questions/19511440/add-b-prefix-to-python-variable
# write data to connected device based on option selected on right menu

"""
  * 1 - Go to position and hold:
  *     h(position),speed,Kp,current_threshold
  *     example: h100,20,3.1,12
  *     
  * 2 - Speed to position and sent flag
  *     s(position),speed
  *     
  * 3 - Gravitiy compensation mode
  *     g(current_threshold),compliance_speed
  *     
  * 4 - Position hold mode
  *     p(Kp),current_threshold
  *     
  * 5 - Speed mode with direction
  *     o(direction 0 or 1),speed
  *     
  * 6 - Jump to position
  *     j(position),Kp,current_threshold
  *    
  *     
  * 7 - Voltage mode
  *     v(direction 0 or 1),voltage(0-1000)

"""
def write_data():
 
    temp = v.get()

    if temp == 1:
        #string_var = "p" + str(e_position.get()) + "," + str(e_speed.get()) + \
         #   "," + str(e_Kp.get()) + "," + str(e_current_tresh.get()) + "\n"

        v1 = str(e_position.get())
        v2 = str(e_speed.get())
        v3 = str(e_Kp.get())
        v4 = str(e_current_tresh.get())

        s.write(b'h')
        s.write(bytes(v1, encoding="ascii"))
        s.write(b',')
        s.write(bytes(v2, encoding="ascii"))
        s.write(b',')
        s.write(bytes(v3, encoding="ascii"))
        s.write(b',')
        s.write(bytes(v4, encoding="ascii"))
        s.write(b'\n')
        #print("s" + str(e_position.get()) + "," + str(e_speed.get()) )

    elif temp == 2:

        v1 = str(e_position.get())
        v2 = str(e_speed.get())

        s.write(b's')
        s.write(bytes(v1, encoding="ascii"))
        s.write(b',')
        s.write(bytes(v2, encoding="ascii"))
        s.write(b'\n')


    elif temp == 3:
        print("g" + str(e_current_tresh.get()) + "," + str(e_comp_speed.get())) 

        v1 = str(e_current_tresh.get())
        v2 = str(e_comp_speed.get())

        s.write(b'g')
        s.write(bytes(v1, encoding="ascii"))
        s.write(b',')
        s.write(bytes(v2, encoding="ascii"))
        s.write(b'\n')
 

    elif temp == 4:

        print("p" + str(e_Kp.get()) + "," + str(e_current_tresh.get()))

        v1 = str(e_Kp.get())
        v2 = str(e_current_tresh.get())

        s.write(b'p')
        s.write(bytes(v1, encoding="ascii"))
        s.write(b',')
        s.write(bytes(v2, encoding="ascii"))
        s.write(b'\n')


    elif temp == 5:

        print("o" + str(e_direction.get()) + "," + str(e_speed.get()))

        v1 = str(e_direction.get())
        v2 = str(e_speed.get())

        s.write(b'o')
        s.write(bytes(v1, encoding="ascii"))
        s.write(b',')
        s.write(bytes(v2, encoding="ascii"))
        s.write(b'\n')

    elif temp == 6:

        print("j" + str(e_position.get()) + "," + str(e_Kp.get() + str(e_current_tresh.get())))

        v1 = str(e_position.get())
        v2 = str(e_Kp.get())
        v3 = str(e_current_tresh.get())

        s.write(b'j')
        s.write(bytes(v1, encoding="ascii"))
        s.write(b',')
        s.write(bytes(v2, encoding="ascii"))
        s.write(b',')
        s.write(bytes(v3, encoding="ascii"))
        s.write(b'\n')


    elif temp == 7:

        print("v" + str(e_direction.get()) + "," + str(e_voltage.get()))

        v1 = str(e_direction.get())
        v2 = str(e_voltage.get())

        s.write(b'v')
        s.write(bytes(v1, encoding="ascii"))
        s.write(b',')
        s.write(bytes(v2, encoding="ascii"))
        s.write(b'\n')


def disable_motor():
    s.write(b'd')
    s.write(b'\n')
    print("d")

def clear_error():
    s.write(b'c')
    s.write(b'\n')
    print("c")

def enable_motor():
    s.write(b'e')
    s.write(b'\n')
    print("e")

# Connect to selected serial port with desired baudrate

def connect_serial():
    global cond
    global connect_cond 
    #cond = True
    if(connect_cond == False):
        s.baudrate = int(baud_e.get())
        s.port = str(com_e.get())
        print(str(com_e.get()))
        s.open()
        s.reset_input_buffer()   
        if(s.is_open == True):
            status2_l = tk.Label(root, text="Connected" , font = "Verdana 10 ", fg = "green")
            status2_l.place(x = 70, y = 200)
            cond = True
            connect_cond = True
            s.write(b'b')
            s.write(b'\n')
            print("b in connect serial")
        else:
            status2_l = tk.Label(root, text="Connected" , font = "Verdana 10 ", fg = "red")
            status2_l.place(x = 70, y = 200)
            cond = False
            connect_cond = False


# disconect from serial port

def plot_stop():
    global cond
    cond = False
    s.close()

# Switch what graph to show and set them up

def switch_graphs(mode_var):

    global data
    global mode_variable
    mode_variable = mode_var
    data_temp = {}
    for i in range(6):
        data_temp[i] = data[i]
        data[i] = np.empty(shape=(1,0))
        lines[i].set_xdata(np.arange(0,len(data[i])))
        lines[i].set_ydata(data[i])

    for i in range(6):
        data[i] = data_temp[i]

    if mode_variable == 1:
        lines[0].set_color('red')
        ax.set_title('Motor position')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Positon in encoder ticks')
        ax.set_xlim(0,210)
        ## do something
    elif mode_variable == 2:
        lines[1].set_color('blue')
        ax.set_title('Motor current')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Current [mA]')
        ax.set_xlim(0,210)
        ax.set_ylim(0,3000)
        ## do something
    elif mode_variable == 3:
        lines[2].set_color('purple')
        ax.set_title('Motor speed')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Speed in RPM')
        ax.set_xlim(0,210)
        ax.set_ylim(-700,700)
        ## do something
    elif mode_variable == 4:
        lines[3].set_color('orange')
        ax.set_title('Serial Data')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Temperature')
        ax.set_xlim(0,210)
        ax.set_ylim(-10,100)
        ## do something 
    elif mode_variable == 5:
        lines[4].set_color('grey')
        ax.set_title('Serial Data')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Voltage [mV]')
        ax.set_xlim(0,210)
        ax.set_ylim(0,3200)
        ## do something
    elif mode_variable == 6:
        lines[5].set_color('black')
        ax.set_title('Serial Data')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Voltage [mV]')
        ax.set_xlim(0,210)
        ax.set_ylim(0,2500)
        ## do something         
    elif mode_variable == 7:
        lines[0].set_color('red')
        lines[1].set_color('blue')
        lines[2].set_color('purple')
        ax.set_title('Serial Data')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Voltage,Position,Current')
        #fig.legend((lines[0],lines[1],lines[2]),('First line', 'Second line', 'Third Line '), 'upper right' , prop={'size': 7})
        ## do something    

    canvas.draw()
      
#Open webpage 
def OpenUrl(url):
    webbrowser.open_new(url)


#Figure canvas for plot
fig = Figure()
ax = fig.add_subplot(111)

# Default mode is postion mode
ax.set_title('Serial Data')
ax.set_xlabel('Sample')
ax.set_ylabel('Positon in encoder ticks')
ax.set_xlim(0,210)
ax.set_ylim(0,1030)

# Every graph line ex. position , current... has its own place in lines dictionary
lines = {}
lines[0] = ax.plot([],[])[0]
lines[1] = ax.plot([],[])[0]
lines[2] = ax.plot([],[])[0]
lines[3] = ax.plot([],[])[0]
lines[4] = ax.plot([],[])[0]
lines[5] = ax.plot([],[])[0]

lines[0].set_color('red')
lines[1].set_color('blue')
lines[2].set_color('purple')
lines[3].set_color('orange')
lines[4].set_color('grey')
lines[5].set_color('black')

# Create canvas for plot 
canvas = FigureCanvasTkAgg(fig, master=root) 
canvas.get_tk_widget().place(x = 200,y=33, width = 900,height = 450)

# Create legend for our graph
fig.legend((lines[0],lines[1],lines[2],lines[3],lines[4]),('Position', 'Current', 'Speed', 'Temperature', 'Voltage[Supply]'),'upper right', prop={'size': 6})

# Create mid , left and right canvas and place some lines on them

mid_canvas = tk.Canvas(root, width = 900,height = 33,bd=1,highlightthickness=0)
mid_canvas.place(x = 200, y = 0)
mid_canvas.create_line(0, 33, 900, 33, fill="black")

left_canvas = tk.Canvas(root, width=200, height=650,bd=1,highlightthickness=0)
left_canvas.place(x = 0, y = 0)
left_canvas.create_line(199, 0, 199, 650, fill="black")

left_canvas.create_line(0, 270, 199, 270, fill="black")
left_canvas.create_line(0, 272, 199, 272, fill="black")

left_canvas.create_line(0, 570, 199, 570, fill="black")
left_canvas.create_line(0, 572, 199, 572, fill="black")

right_canvas = tk.Canvas(root, width=200, height=650,bd=1,highlightthickness=0)
right_canvas.place(x = 1100, y = 0)
right_canvas.create_line(1, 0, 1, 650, fill="black")
right_canvas.create_line(0, 60, 199, 60, fill="black")
right_canvas.create_line(0, 62, 199, 62, fill="black")

# Create toolbaar so you can zoom and move around in plots
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()

# Left side of screen
# Here we define all labels, buttons and entries for the left side of the screen

tel = tk.Label(root, text="Telemetry" , font = "Verdana 12 bold")
tel.place(x = 10, y = 237)

com_l = tk.Label(root, text="COM Port:" , font = "Verdana 14 ")
com_l.place(x = 10, y = 30)

com_e = tk.Entry(root,width = 15, borderwidth = 5)
com_e.place(x = 10, y = 65)

baud_l = tk.Label(root, text="Baudrate:" , font = "Verdana 14 ")
baud_l.place(x = 10, y = 95)

baud_e = tk.Entry(root,width = 15, borderwidth = 5)
baud_e.place(x = 10, y = 125)

root.update()
connect = tk.Button(root, text = "Connect", font = ('calbiri',12),activebackground = "green",height = 1 , command = lambda: connect_serial())
connect.place(x = 10, y = 160 )

status_l = tk.Label(root, text="Status: " , font = "Verdana 10 ")
status_l.place(x = 10, y = 200)

status2_l = tk.Label(root, text="Connected" , font = "Verdana 10 ", fg = "red")
status2_l.place(x = 70, y = 200)

root.update()
start = tk.Button(root, text = "Start", font = ('calbiri',12),activebackground = "green",height = 1 , command = lambda: plot_start())
start.place(x = 4, y = 530 )

root.update()
pause = tk.Button(root, text = "Pause", font = ('calbiri',12), activebackground = "red", command = lambda:plot_stop())
pause.place(x = start.winfo_x()+start.winfo_reqwidth() + 10, y = 530)




#image = Image.open("C:\\Users\\xxxx\\Desktop\\python_gui\\donate_button.png")
#photo = ImageTk.PhotoImage(image)

#b_donate = tk.Button(root, image=photo, command=lambda aurl=url_donate:OpenUrl_donate(aurl) )
#b_donate.place(x = 30, y = 570)

# Middle of the screen
# Here we define all labels, buttons and entries for the middle side of the screen

version_l = tk.Label(root, text = version_txt , font = "Verdana 10 ", fg = "black")
version_l.place(x = 960, y = 600)

root.update()

get_user_guide = tk.Button(root, text = "User guide", font = ('calbiri',12),activebackground = "green",height = 1 , command=lambda aurl=url_user_guide:OpenUrl(aurl))
get_user_guide.place(x = 420, y = 600 )

get_forum = tk.Button(root, text = "Forum", font = ('calbiri',12),activebackground = "green",height = 1 , command=lambda aurl=url_forum:OpenUrl(aurl))
get_forum.place(x = 360, y = 600 )

get_github = tk.Button(root, text = "Github", font = ('calbiri',12),activebackground = "green",height = 1 , command=lambda aurl=url_github:OpenUrl(aurl))
get_github.place(x = 300, y = 600 )

get_help = tk.Button(root, text = "Help", font = ('calbiri',12),activebackground = "green",height = 1 , command=lambda aurl=url_help:OpenUrl(aurl))
get_help.place(x = 250, y = 600 )

graph_l = tk.Label(root, text="Choose graph:" , font = "Verdana 14 ")
graph_l.place(x = 230, y = 1)

root.update()
position_b = tk.Button(root, text = "Position", font = ('calbiri',12) , width = 7, command=lambda *args: switch_graphs(1))
position_b.place(x = 425, y = 1)

root.update()
current_b = tk.Button(root, text = "Current", font = ('calbiri',12) , width = 7, command=lambda *args: switch_graphs(2))
current_b.place(x = position_b.winfo_x()+position_b.winfo_reqwidth() + 1, y = 1)

root.update()
speed_b = tk.Button(root, text = "Speed", font = ('calbiri',12) , command=lambda *args: switch_graphs(3) )
speed_b.place(x = current_b.winfo_x()+current_b.winfo_reqwidth() + 1, y = 1)

root.update()
temperature_b = tk.Button(root, text = "Temperature", font = ('calbiri',12), command=lambda *args: switch_graphs(4) )
temperature_b.place(x = speed_b.winfo_x()+speed_b.winfo_reqwidth() + 1, y = 1)

root.update()
supply_b = tk.Button(root, text = "Supply voltage", font = ('calbiri',12), command=lambda *args: switch_graphs(5) )
supply_b.place(x = temperature_b.winfo_x()+temperature_b.winfo_reqwidth() + 1, y = 1)

#root.update()
#BEMF_b = tk.Button(root, text = "BEMF", font = ('calbiri',12) , command=lambda *args: switch_graphs(6))
#BEMF_b.place(x = supply_b.winfo_x()+supply_b.winfo_reqwidth() + 1, y = 1)

root.update()
multi_b = tk.Button(root, text = "Current, Position, Speed", font = ('calbiri',12), command=lambda *args: switch_graphs(7) )
multi_b .place(x = supply_b.winfo_x() + supply_b.winfo_reqwidth() + 1, y = 1)

# Right side of the screen
# Here we define all labels, buttons and entries for the right side of the screen

root.update()
control_l = tk.Label(root, text="Control Panel" , font = "Verdana 14 ")
control_l.place(x = 1110, y = 30)

root.update()
disable_b = tk.Button(root, text = "Motor disable", font = ('calbiri',12), activebackground = "red", width = 19, command = lambda:disable_motor() )
disable_b .place(x =1110, y = 65)

enable_b = tk.Button(root, text = "Motor enable", font = ('calbiri',12), activebackground = "green", width = 19, command = lambda:enable_motor() )
enable_b .place(x =1110, y = 100)

clear_error_b = tk.Button(root, text = "Clear error", font = ('calbiri',12), activebackground = "yellow", width = 19, command = lambda:clear_error() )
clear_error_b .place(x =1110, y = 135)

# Control panel menu on the right side of the screen

option_positon = tk.Label()
option_speed = tk.Label()
option_Kp = tk.Label()
option_current_tresh = tk.Label()
option_direction = tk.Label()
option_Compliance_speed = tk.Label()
option_voltage = tk.Label()

e_position = tk.Entry()
e_speed = tk.Entry()
e_Kp = tk.Entry()
e_current_tresh = tk.Entry()
e_direction = tk.Entry()
e_comp_speed = tk.Entry()
e_voltage = tk.Entry()

Send_b = tk.Button()

v = tk.IntVar()

# Create radio button entry on the 
for operation_mode, mode_number in Modes:
     tk.Radiobutton(root, 
                  text=operation_mode,
                  indicatoron = 0,
                  width = 20,
                  padx = 20, 
                  variable=v, 
                  borderwidth = 5,
                  command=lambda: control_panel_menu(),
                  value=mode_number).place(x = 1105, y = 150 + mode_number * 25)

# Main loop
root.after(1,plot_data)
root.mainloop()
