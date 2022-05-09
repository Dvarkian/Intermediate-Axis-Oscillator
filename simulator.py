import PySimpleGUI as sg
import os

import time
import math
import random

textCol = "light blue"
textInpCol = "grey90"
bgCol = "grey15"
fieldCol = "grey4"
axisCol = "grey30"

omega1Col = "yellow"
omega2Col = "green1"
omega3Col = "orange"

inputLen = 15

graphHeight = 10

layout = [[sg.Column([[sg.Text("Moments of Inertia (kgm²):", text_color=textCol, background_color=bgCol)],
                      [sg.Text("I₁:", text_color=omega1Col, background_color=bgCol),
                       sg.Input("0.0001266726583", size=(inputLen, 1), text_color=omega1Col, background_color=fieldCol, key="-I1-")],
                      [sg.Text("I₂:", text_color=omega2Col, background_color=bgCol),
                       sg.Input("0.000491276325", size=(inputLen, 1), text_color=omega2Col, background_color=fieldCol, key="-I2-")],
                      [sg.Text("I₃:", text_color=omega3Col, background_color=bgCol),
                       sg.Input("0.0006119417833", size=(inputLen, 1), text_color=omega3Col, background_color=fieldCol, key="-I3-")]],
                     background_color=bgCol),
           sg.VerticalSeparator(),
           sg.Column([[sg.Text("Torques (Nm):", text_color=textCol, background_color=bgCol)],
                      [sg.Text("K₁:", text_color=omega1Col, background_color=bgCol),
                       sg.Input("0", size=(inputLen, 1), text_color=omega1Col, background_color=fieldCol, key="-K1-")],
                      [sg.Text("K₂:", text_color=omega2Col, background_color=bgCol),
                       sg.Input("0", size=(inputLen, 1), text_color=omega2Col, background_color=fieldCol, key="-K2-")],
                      [sg.Text("K₃:", text_color=omega3Col, background_color=bgCol),
                       sg.Input("0", size=(inputLen, 1), text_color=omega3Col, background_color=fieldCol, key="-K3-")]],
                     background_color=bgCol),
           sg.VerticalSeparator(),
           sg.Column([[sg.Text("Initial Angular Velocities (rad/s):", text_color=textCol, background_color=bgCol)],
                      [sg.Text("ω₁:", text_color=omega1Col, background_color=bgCol),
                       sg.Input("0.001", size=(inputLen, 1), text_color=omega1Col, background_color=fieldCol, key="-O1-")],
                      [sg.Text("ω₂:", text_color=omega2Col, background_color=bgCol),
                       sg.Input("2", size=(inputLen, 1), text_color=omega2Col, background_color=fieldCol, key="-O2-")],
                      [sg.Text("ω₃:", text_color=omega3Col, background_color=bgCol),
                       sg.Input("0.001", size=(inputLen, 1), text_color=omega3Col, background_color=fieldCol, key="-O3-")]],
                     background_color=bgCol),
           sg.VerticalSeparator(),
           sg.Column([[sg.Text("Other Parameters:", text_color=textCol, background_color=bgCol)],
                      [sg.Text("Graph Length (s):", text_color=textCol, background_color=bgCol),
                       sg.Input("40", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-LEN-")],
                      [sg.Text("Time Step (s/it):", text_color=textCol, background_color=bgCol),
                       sg.Input("0.05", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-RES-")],
                      [sg.Text("Perturbation Duration (s):", text_color=textCol, background_color=bgCol),
                       sg.Input("0.0", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-KDUR-")]],
                     background_color=bgCol)],
          [sg.Graph((1000, 500), (0, -40), (10, 40), "grey10", key="-GRAPH-")],
          [sg.Button("Graph Angular Velocity vs. Time.", button_color=("grey4", "green1"), key="-GO-"),
           sg.ProgressBar(100, "h", size_px=(100, 6), key="-BAR-", bar_color=("green1", "grey4"), relief="RELIEF_RAISED")]]

window = sg.Window("Intermediate Axis Simulator",
                   layout,
                   background_color=bgCol,
                   finalize=True)

                      
window["-BAR-"].update(visible=False)

i = 1

def graphState(K1, K2, K3, I1, I2, I3, Omega1_start, Omega2_start, Omega3_start, dt, t_end, perturbationDuration):

    graphHeight = int(max([Omega1_start, Omega2_start, Omega3_start]) * 5)

    #window["-BAR-"].update(visible=True)
    window.refresh()

    window["-GRAPH-"].change_coordinates((0, -graphHeight), (t_end, graphHeight))

    window["-GRAPH-"].DrawLine((0, -graphHeight), (0, graphHeight), axisCol, 1)
    window["-GRAPH-"].DrawLine((0, 0), (t_end, 0), axisCol, 1)

    for y in range(-graphHeight, graphHeight):
        if y % (graphHeight / 10) == 0:
            window["-GRAPH-"].DrawLine((0, y), (dt*t_end/2, y), axisCol)
            window["-GRAPH-"].DrawText(str(y), (dt*t_end, y), axisCol)
        else:
            window["-GRAPH-"].DrawLine((0, y), (dt*t_end/4, y), axisCol)

    

    t_arr = [0]
    
    Omega1_arr = [Omega1_start]
    Omega2_arr = [Omega2_start]
    Omega3_arr = [Omega3_start]

    i = 0

    window["-GRAPH-"].DrawLine((0, 0), (10, 0), axisCol, 1)

    while t_arr[i-1] < t_end:

        if perturbationDuration != 0:
            if t_arr[i-1] > perturbationDuration:
                K1, K2, K3 = 0, 0, 0

        #print(t_arr[i-1])

        window["-BAR-"].update(int(t_arr[i-1]*100 / 10))
        window.refresh()
        
        Omega1 = Omega1_arr[i-1]
        Omega2 = Omega2_arr[i-1]
        Omega3 = Omega3_arr[i-1]
       
        t = t_arr[i-1]
       
        dOmega1dt = (K1 - (I3 - I2)*Omega2*Omega3) / I1 # calculate the derivative of Omega1
        dOmega2dt = (K2 - (I1 - I3)*Omega1*Omega3) / I2  # calculate the derivative of Omega1
        dOmega3dt = (K3 - (I2 - I1)*Omega2*Omega1) / I3


        if abs(math.modf(t_arr[i-1])[0] < dt):
            window["-GRAPH-"].DrawLine((t_arr[i-1], -(1/40)*graphHeight), (t_arr[i-1], (1/40)*graphHeight), axisCol, 1)
            window["-GRAPH-"].DrawText(str(int(math.modf(t_arr[i-1])[1])), (t_arr[i-1], (-1/20)*graphHeight), axisCol)
        elif abs(math.modf(t_arr[i-1])[0] - 0.5) < dt/2:
            window["-GRAPH-"].DrawLine((t_arr[i-1], -(1/80)*graphHeight), (t_arr[i-1], (1/80)*graphHeight), axisCol, 1)
        #else:
        #    window["-GRAPH-"].DrawLine((t_arr[i-1], -0.2), (t_arr[i-1], 0.2), axisCol, 1)

       
        Omega1_arr.append(Omega1 + dt*dOmega1dt)  # calc. Omega1 at next timestep,add to array
        Omega2_arr.append(Omega2 + dt*dOmega2dt)  # calc. Omega2 at next timestep,add to array
        Omega3_arr.append(Omega3 + dt*dOmega3dt)  # calc. Omega2 at next timestep,add to array

        t_arr.append(t + dt)       # add new value of t to array

        #window["-GRAPH-"].DrawLine(((i-1)*dt*timescale, Omega1_arr[i-1]), ((i)*dt*timescale, Omega1_arr[i]), "yellow", 1)
        window["-GRAPH-"].DrawLine((t_arr[i-1], Omega1_arr[i-1]), (t_arr[i], Omega1_arr[i]), "yellow", 1)
        window["-GRAPH-"].DrawLine((t_arr[i-1], Omega2_arr[i-1]), (t_arr[i], Omega2_arr[i]), "orange", 1)
        window["-GRAPH-"].DrawLine((t_arr[i-1], Omega3_arr[i-1]), (t_arr[i], Omega3_arr[i]), "green1", 1)

       


        

        i += 1

    window["-BAR-"].update(visible=False)
    window.refresh()



while True:

    event, values = window.read(timeout=0)

    if event == sg.WIN_CLOSED:
        break

    try:
        K1, K2, K3, = float(values["-K1-"]),  float(values["-K2-"]),  float(values["-K3-"])
        I1, I2, I3, = float(values["-I1-"]),  float(values["-I2-"]),  float(values["-I3-"])
        O1, O2, O3, = float(values["-O1-"]),  float(values["-O2-"]),  float(values["-O3-"])
        length, timeStep, perturbationDuration = float(values["-LEN-"]),  float(values["-RES-"]), float(values["-KDUR-"])
        
    except ValueError:
        print("Invalid cell.")
        continue

    
    if event == "-GO-":
        window["-GRAPH-"].erase()
        graphState(K1, K2, K3, I1, I2, I3, O1, O2, O3, timeStep, length, perturbationDuration)




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
