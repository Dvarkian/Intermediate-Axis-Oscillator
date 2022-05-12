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

filepaths = []

I1 = 0.0001266726583
I2 = 0.000491276325
I3 = 0.0006119417833

timeStep = 0.05
t_end = 40

for root, dirs, files in os.walk('data'):
    # select file name
    for file in files:
        # check the extension of files
        if file.endswith('.csv') and "meta" not in root:
            # print whole path of files
            filepath = os.path.join(root, file)
            filepaths.append(filepath)


colLayout = [[sg.Column([[sg.Text("Moments of Inertia (kgm²):", text_color=textCol, background_color=bgCol)],
                      [sg.Text("I₁:", text_color=omega1Col, background_color=bgCol),
                       sg.Input(str(I1), size=(inputLen, 1), text_color=omega1Col, background_color=fieldCol, key="-I1-")],
                      [sg.Text("I₂:", text_color=omega2Col, background_color=bgCol),
                       sg.Input(str(I2), size=(inputLen, 1), text_color=omega2Col, background_color=fieldCol, key="-I2-")],
                      [sg.Text("I₃:", text_color=omega3Col, background_color=bgCol),
                       sg.Input(str(I3), size=(inputLen, 1), text_color=omega3Col, background_color=fieldCol, key="-I3-")]],
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
                       sg.Input(str(t_end), size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-LEN-")],
                      [sg.Text("Time Step (s/it):", text_color=textCol, background_color=bgCol),
                       sg.Input(str(timeStep), size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-RES-")],
                      [sg.Text("Perturbation Duration (s):", text_color=textCol, background_color=bgCol),
                       sg.Input("0.0", size=(inputLen, 1), text_color=textInpCol, background_color=fieldCol, key="-KDUR-")]],
                     background_color=bgCol)],[sg.Graph((820, 400), (0, -40), (10, 40), "grey10", key="-GRAPH-")],
             [sg.Button("Graph Angular Velocity vs. Time.", button_color=("grey4", "green1"), key="-GO-"),
              sg.ProgressBar(100, "h", size_px=(100, 6), key="-BAR-", bar_color=("green1", "grey4"), relief="RELIEF_RAISED")],
             [sg.HorizontalSeparator()]]


for i in range(0, len(filepaths)):
    colLayout.append([sg.Text(filepaths[i])])
    colLayout.append([sg.Graph((820, 180), (0, -50), (150, 50), "grey10", key="-GRAPH" + str(i) + "-")])
    colLayout.append([sg.Text("Initial Conditions:", background_color=bgCol, text_color=textCol, pad=((2, 2), (0, 17))),
                      sg.Text("ω₁=", text_color=omega1Col, background_color=bgCol, pad=((2, 2), (0, 17)),
                              k="-INIT1" + str(i) + "-"),
                      sg.Text("ω₂=", text_color=omega2Col, background_color=bgCol, pad=((2, 2), (0, 17)),
                              k="-INIT2" + str(i) + "-"),
                      sg.Text("ω₃=", text_color=omega3Col, background_color=bgCol, pad=((2, 2), (0, 17)),
                              k="-INIT3" + str(i) + "-")]
                     )


layout = [[sg.Col(colLayout, bgCol, (950, 800), key="-COL-", scrollable=True, element_justification="center",
                  vertical_scroll_only=True)]]


                      
window = sg.Window("Intermediate Axis Simulator",
                   layout,
                   background_color="grey9",
                   finalize=True,
                   size=(920, 800),
                   margins=(2, 2))


window["-BAR-"].update(visible=False)

i = 1

def graphState(K1, K2, K3, I1, I2, I3, Omega1_start, Omega2_start, Omega3_start, dt, t_end, perturbationDuration, graph,
               Omega2a_start, Omega1a_start, Omega3a_start):

    graph = window["-GRAPH-"]

    graphHeight = int(max([Omega1_start, Omega2_start, Omega3_start]) * 3)

    window.refresh()

    graph.change_coordinates((0, -graphHeight), (t_end, graphHeight))

    graph.DrawLine((0, -graphHeight), (0, graphHeight), axisCol, 1)
    graph.DrawLine((0, 0), (t_end, 0), axisCol, 1)

    for y in range(-graphHeight, graphHeight):
        if y % (graphHeight / 10) == 0:
            graph.DrawLine((0, y), (dt*t_end/4, y), axisCol)
            graph.DrawText(str(y), (dt*t_end/2, y), axisCol)
        else:
            graph.DrawLine((0, y), (dt*t_end/4, y), axisCol)
        
    timeArray = [0]

    Omega1_arr = [Omega1_start]
    Omega2_arr = [Omega2_start]
    Omega3_arr = [Omega3_start]

    i = 1

    graph.DrawLine((0, 0), (10, 0), axisCol, 1)

    while timeArray[i-1] < t_end:

        if perturbationDuration != 0:
            if timeArray[i-1] > perturbationDuration:
                K1, K2, K3 = 0, 0, 0

        window.refresh()
        
        Omega1 = Omega1_arr[i-1]
        Omega2 = Omega2_arr[i-1]
        Omega3 = Omega3_arr[i-1]
       
        t = timeArray[i-1]
       
        dOmega1dt = (K1 - (I3 - I2)*Omega2*Omega3) / I1 # calculate the derivative of Omega1
        dOmega2dt = (K2 - (I1 - I3)*Omega1*Omega3) / I2  # calculate the derivative of Omega1
        dOmega3dt = (K3 - (I2 - I1)*Omega2*Omega1) / I3

        if graph == window["-GRAPH-"]:
            if abs(math.modf(timeArray[i-1])[0] < dt):
                graph.DrawLine((timeArray[i-1], -(1/40)*graphHeight), (timeArray[i-1], (1/40)*graphHeight), axisCol, 1)
                graph.DrawText(str(int(math.modf(timeArray[i-1])[1])), (timeArray[i-1], (-1/20)*graphHeight), axisCol)
            elif abs(math.modf(timeArray[i-1])[0] - 0.5) < dt/2:
                graph.DrawLine((timeArray[i-1], -(1/80)*graphHeight), (timeArray[i-1], (1/80)*graphHeight), axisCol, 1)

        Omega1_arr.append(Omega1 + dt*dOmega1dt)  # calc. Omega1 at next timestep,add to array
        Omega2_arr.append(Omega2 + dt*dOmega2dt)  # calc. Omega2 at next timestep,add to array
        Omega3_arr.append(Omega3 + dt*dOmega3dt)  # calc. Omega2 at next timestep,add to array

        timeArray.append(t + dt)       # add new value of t to array

        graph.DrawLine((timeArray[i-1], Omega1_arr[i-1]), (timeArray[i], Omega1_arr[i]), "yellow", 1)
        graph.DrawLine((timeArray[i-1], Omega2_arr[i-1]), (timeArray[i], Omega2_arr[i]), "orange", 1)
        graph.DrawLine((timeArray[i-1], Omega3_arr[i-1]), (timeArray[i], Omega3_arr[i]), "green1", 1)

        i += 1

    window.refresh()



window.refresh()

print("Done.")

t = -100

header = True

init1 = 0
init2 = 0
init3 = 0

heightThreshold = 13
# 10 too low

for dataIndex in range(0, len(filepaths)):
    startFound = False
    startTime = 0
    endFound = False
    endTime = 0
    data = []
    lastxw = [0, 0]
    lastyw = [0, 0]
    lastzw = [0, 0]
    validData = 0

    xA = 0
    yA = 0
    zA = 0

    graphHeight = 40

    window["-GRAPH" + str(dataIndex) + "-"].change_coordinates((0, -graphHeight), (6, graphHeight))

    window["-GRAPH" + str(dataIndex) + "-"].DrawLine((0, 0), (500, 0), axisCol, 1)
    
    with open(filepaths[dataIndex], "r") as file:
        data = file.readlines()[1:]

    for i in range(1, 1000, 10):
        window["-GRAPH" + str(dataIndex) + "-"].DrawLine((i, -6), (i, 6), axisCol, 1)

    timeArray = [0]

    startIndex = 0
    dataPointStartIndex = 0

    firstFind = None

    for p in range(0, 20, 1):
        window["-GRAPH" + str(dataIndex) + "-"].DrawLine((p, -5), (p, 5), "red", 1)


    startTime1 = 0
        
    for dataPointIndex in range(0, len(data)):
        time, xw, yw, zw, absw = data[dataPointIndex].split(",")
        time, xw, yw, zw, absw = float(time)-1, float(xw), float(yw), float(zw), float(absw)

        xSlope = (xw-lastxw[1]) / (time - startTime1 - lastxw[0])
        ySlope = (yw-lastyw[1]) / (time - startTime1 - lastyw[0])
        zSlope = (zw-lastzw[1]) / (time - startTime1 - lastzw[0])

        maxSlope = max(abs(xSlope), abs(ySlope), abs(zSlope))

        dataIndex2 = ""

        if abs(xSlope) < 28 and xw > heightThreshold and not startFound :
            window["-GRAPH" + str(dataIndex) + "-"].DrawLine((time, -200), (time, 200), "green1", 1)
            window["-GRAPH" + str(dataIndex) + "-"].DrawLine((time - 0.02, heightThreshold),
                                                              (time + 0.02, heightThreshold), "green", 1)
            startFound = True
            startTime = time

            dataPointStartIndex = dataPointIndex

            xA = xSlope
            yA = ySlope
            zA = zSlope

            print("Starttime:", time)

            window["-INIT1" + str(dataIndex) + "-"].Update("ω₁=" + str(xw)[:6] + " rad/s")
            window["-INIT2" + str(dataIndex) + "-"].Update("ω₂=" + str(yw)[:6] + " rad/s")
            window["-INIT3" + str(dataIndex) + "-"].Update("ω₁=" + str(zw)[:6] + " rad/s")

        if abs(maxSlope) > 650 and startFound and not endFound:
            window["-GRAPH" + str(dataIndex) + "-"].DrawLine((time - startTime1, -100), (time - startTime1, 100), "firebrick1", 1)
            endFound = True
            endTime = time
            #print("Endtime:", time)

        if not endFound:
            window["-GRAPH" + str(dataIndex) + "-"].DrawLine(lastxw, (time - startTime1, xw), "saddle brown", 1)
            lastxw = (time - startTime1, xw)
            window["-GRAPH" + str(dataIndex) + "-"].DrawLine(lastyw, (time - startTime1, yw), "dark red", 1)
            lastyw = (time - startTime1, yw)
            window["-GRAPH" + str(dataIndex) + "-"].DrawLine(lastzw, (time - startTime1, zw), "dark green", 1)
            lastzw = (time - startTime1, zw)

            validData += 1


    sampleLen = 1

    time = startTime

    print("Found!")
    
    Omega1_arr = []
    Omega2_arr = []
    Omega3_arr = []

    for foreIndex in range(dataPointStartIndex, dataPointStartIndex+sampleLen):
        Omega2_arr.append(float(data[dataPointStartIndex].split(",")[1]))
        Omega1_arr.append(float(data[dataPointStartIndex].split(",")[2]))
        Omega3_arr.append(float(data[dataPointStartIndex].split(",")[3]))

    timeArray = [time]

    i = 0
    dt = 0.004

    while timeArray[i-1] < endTime:
        window.refresh()

        Omega1 = Omega1_arr[i-1]
        Omega2 = Omega2_arr[i-1]
        Omega3 = Omega3_arr[i-1]

        t = timeArray[i-1]

        dOmega1dt = (0 - (I3 - I2)*Omega2*Omega3) / I1*-1 # calculate the derivative of Omega1
        dOmega2dt = (0 - (I1 - I3)*Omega1*Omega3) / I2*-1  # calculate the derivative of Omega1
        dOmega3dt = (0 - (I2 - I1)*Omega2*Omega1) / I3*-1
     
        Omega1_arr.append(Omega1 + dt*dOmega1dt)  # calc. Omega1 at next timestep,add to array
        Omega2_arr.append(Omega2 + dt*dOmega2dt)  # calc. Omega2 at next timestep,add to array
        Omega3_arr.append(Omega3 + dt*dOmega3dt)  # calc. Omega2 at next timestep,add to array

        timeArray.append(t + dt)       # add new value of t to array

        #window["-GRAPH-"].DrawLine(((i-1)*dt*timescale, Omega1_arr[i-1]), ((i)*dt*timescale, Omega1_arr[i]), "yellow", 1)
        
        window["-GRAPH" + str(dataIndex) + "-"].DrawLine((timeArray[i-1], Omega1_arr[i-1]), (timeArray[i], Omega1_arr[i]), "red", 1)
        window["-GRAPH" + str(dataIndex) + "-"].DrawLine((timeArray[i-1], Omega2_arr[i-1]), (timeArray[i], Omega2_arr[i]), "orange", 1)
        window["-GRAPH" + str(dataIndex) + "-"].DrawLine((timeArray[i-1], Omega3_arr[i-1]), (timeArray[i], Omega3_arr[i]), "green1", 1)

        i += 1
        


while True:

    event, values = window.read(timeout=0)

    if event == sg.WIN_CLOSED:
        break

    try:
        K1, K2, K3, = float(values["-K1-"]),  float(values["-K2-"]),  float(values["-K3-"])
        I1, I2, I3, = float(values["-I1-"]),  float(values["-I2-"]),  float(values["-I3-"])
        O1, O2, O3, = float(values["-O1-"]),  float(values["-O2-"]),  float(values["-O3-"])
        t_end, timeStep, perturbationDuration = float(values["-LEN-"]),  float(values["-RES-"]), float(values["-KDUR-"])
        
    except ValueError:
        continue
    
    if event == "-GO-":
        window["-GRAPH-"].erase()
        graphState(K1, K2, K3, I1, I2, I3, O1, O2, O3, timeStep, t_end, perturbationDuration, window["-GRAPH-"], 0, 0, 0)


