import PySimpleGUI as sg
import os

import time

import random

textCol = "light blue"
textInpCol = "orange"
bgCol = "grey15"
fieldCol = "grey4"
inputLen = 15

layout = [[sg.Column([[sg.Text("Moments of Inertia:", text_color=textCol, background_color=bgCol)],
                      [sg.Text("I 1:", text_color=textCol, background_color=bgCol),
                       sg.Input("0.0001266726583", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-I1-")],
                      [sg.Text("I 2:", text_color=textCol, background_color=bgCol),
                       sg.Input("0.000491276325", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-I2-")],
                      [sg.Text("I 3:", text_color=textCol, background_color=bgCol),
                       sg.Input("0.0006119417833", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-I3-")]],
                     background_color=bgCol),
           sg.VerticalSeparator(),
           sg.Column([[sg.Text("Purterbation Torque:", text_color=textCol, background_color=bgCol)],
                      [sg.Text("K 1:", text_color=textCol, background_color=bgCol),
                       sg.Input("0", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-K1-")],
                      [sg.Text("K 2:", text_color=textCol, background_color=bgCol),
                       sg.Input("0", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-K2-")],
                      [sg.Text("K 3:", text_color=textCol, background_color=bgCol),
                       sg.Input("0", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-K3-")]],
                     background_color=bgCol),
           sg.VerticalSeparator(),
           sg.Column([[sg.Text("Initial Positions:", text_color=textCol, background_color=bgCol)],
                      [sg.Text("Ω 1:", text_color=textCol, background_color=bgCol),
                       sg.Input("2", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-O1-")],
                      [sg.Text("Ω 2:", text_color=textCol, background_color=bgCol),
                       sg.Input("2", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-O2-")],
                      [sg.Text("Ω 3:", text_color=textCol, background_color=bgCol),
                       sg.Input("2", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-O3-")]],
                     background_color=bgCol),
           sg.VerticalSeparator(),
           sg.Column([[sg.Text("Other Parameters:", text_color=textCol, background_color=bgCol)],
                      [sg.Text("Graph Length (s):", text_color=textCol, background_color=bgCol),
                       sg.Input("10", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-LEN-")],
                      [sg.Text("Time Step (s):", text_color=textCol, background_color=bgCol),
                       sg.Input("0.001", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-RES-")],
                      [sg.Text("Perturbation Duration (s):", text_color=textCol, background_color=bgCol),
                       sg.Input("0.001", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-KT-")]],
                     background_color=bgCol)],
          [sg.Graph((1000, 500), (0, -40), (20, 40), "grey10", key="-GRAPH-")],
          [sg.Button("Generate Results!", button_color=("grey4", "green1"), key="-GO-")]]

window = sg.Window("Intermediate Axis Simulator",
                   layout,
                   background_color=bgCol,
                   finalize=True)

                      

# Euler's method

i = 1


I3 = 0.0006119417833
I2 = 0.000491276325
I1 = 0.0001266726583

#Dt = 0.01 # timestep Delta t



#t_start = 0             # starttime
#t_end = 10              # endtimen_steps = int(round((t_end-t_start)/Dt))    # number of timesteps


#K1 = 0.0000    
#K2 = 0.0000
#K3 = 0.0000

#Omega1_start = 2          # initial Omega1
#Omega2_start = 2        # initial Omega2
#Omega3_start = 2        # initial Omega2

def graphState(K1, K2, K3, KT, I1, I2, I3, Omega1_start, Omega2_start, Omega3_start, Dt, t_end):

    t_arr = [0]
    
    Omega1_arr = [Omega1_start]
    Omega2_arr = [Omega2_start]
    Omega3_arr = [Omega3_start]

    i = 0

    while t_arr[i-1] < 100:
        
        Omega1 = Omega1_arr[i-1]
        Omega2 = Omega2_arr[i-1]
        Omega3 = Omega3_arr[i-1]
       
        t = t_arr[i-1]
       
        dOmega1dt = (K1 - (I3 - I2)*Omega2*Omega3) / I1 # calculate the derivative of Omega1
        dOmega2dt = (K2 - (I1 - I3)*Omega1*Omega3) / I2  # calculate the derivative of Omega1
        dOmega3dt = (K3 - (I2 - I1)*Omega2*Omega1) / I3

       
        Omega1_arr.append(Omega1 + Dt*dOmega1dt)  # calc. Omega1 at next timestep,add to array
        Omega2_arr.append(Omega2 + Dt*dOmega2dt)  # calc. Omega2 at next timestep,add to array
        Omega3_arr.append(Omega3 + Dt*dOmega3dt)  # calc. Omega2 at next timestep,add to array

        t_arr.append(t + Dt)       # add new value of t to array


        #window["-GRAPH-"].DrawLine(((i-1)*Dt*timescale, Omega1_arr[i-1]), ((i)*Dt*timescale, Omega1_arr[i]), "yellow", 1)
        window["-GRAPH-"].DrawLine((t_arr[i-1], Omega1_arr[i-1]), (t_arr[i], Omega1_arr[i]), "yellow", 1)
        window["-GRAPH-"].DrawLine((t_arr[i-1], Omega2_arr[i-1]), (t_arr[i], Omega2_arr[i]), "orange", 1)
        window["-GRAPH-"].DrawLine((t_arr[i-1], Omega3_arr[i-1]), (t_arr[i], Omega3_arr[i]), "green1", 1)
        

        i += 1


oldParams = []

while True:

    event, values = window.read(timeout=0)

    if event == sg.WIN_CLOSED:
        break

    try:
        K1, K2, K3, = float(values["-K1-"]),  float(values["-K2-"]),  float(values["-K3-"])
        I1, I2, I3, = float(values["-I1-"]),  float(values["-I2-"]),  float(values["-I3-"])
        O1, O2, O3, = float(values["-O1-"]),  float(values["-O2-"]),  float(values["-O3-"])
        length, step, KT = float(values["-LEN-"]),  float(values["-RES-"]), float(values["-KT-"])
        
    except ValueError:
        print("Invalid cell.")
        continue

    
    if event == "-GO-":
        window["-GRAPH-"].erase()
        graphState(K1, K2, K3, KT, I1, I2, I3, O1, O2, O3, step, length)




"""
filepaths = []

for root, dirs, files in os.walk('data'):
    # select file name
    for file in files:
        # check the extension of files
        if file.endswith('.csv') and "meta" not in root:
            # print whole path of files
            filepath = os.path.join(root, file)
            filepaths.append(filepath)

colLayout = []

for i in range(0, len(filepaths)):
    colLayout.append([sg.Text(filepaths[i])])
    colLayout.append([sg.Graph((800, 200), (0, -60), (800, 60), "grey10", key="-GRAPH" + str(i) + "-")])

layout = [[sg.Col(colLayout, "grey30", (800, 800), key="-COL-", scrollable=True, element_justification="center")]]

window = sg.Window("Intermediate Axis Simulator",
                   layout,
                   background_color="grey9",
                   finalize=True)

window.refresh()

print("Done.")

t = -100

header = True

data = []
lastxw = [0, 0]
lastyw = [0, 0]
lastzw = [0, 0]


for dataIndex in range(0, len(filepaths)):
    with open(filepaths[dataIndex], "r") as file:
        data = file.readlines()[1:]

    for i in range(1, 1000, 10):
        window["-GRAOmega2H" + str(dataIndex) + "-"].DrawLine((i, -100), (i, 100), "grey15", 1)
        
    for dataOmega2oint in data:
        time, xw, yw, zw, absw = dataOmega2oint.split(",")
        time, xw, yw, zw, absw = float(time)*100, float(xw), float(yw), float(zw), float(absw)

        window["-GRAOmega2H" + str(dataIndex) + "-"].DrawLine(lastxw, (time, xw), "green1", 2)
        lastxw = (time, xw)
        window["-GRAOmega2H" + str(dataIndex) + "-"].DrawLine(lastyw, (time, yw), "light blue", 2)
        lastyw = (time, yw)
        window["-GRAOmega2H" + str(dataIndex) + "-"].DrawLine(lastzw, (time, zw), "yellow", 2)
        lastzw = (time, zw)


#window["-GRAPH-"].DrawLine((-800, 0), (800, 0), "grey20", 1)


while True:
    event, values = window.read(timeout=10)

    if event == sg.WIN_CLOSED:
        break

    t += 1
"""
