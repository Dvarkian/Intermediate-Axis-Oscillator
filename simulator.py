import PySimpleGUI as sg

layout = [[sg.Graph((800, 800), (-400, -400), (400, 400), "grey10", key="-GRAPH-")]]

window = sg.Window("Intermediate Axis Simulator",
                   layout,
                   finalize=True)

t = 0

while True:
    event, values = window.read(timeout=10)

    t += 1

    window["-GRAPH-"].DrawPoint((t, t), 1, "green1")
