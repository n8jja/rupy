import PySimpleGUI as sg

# Create layouts here
# Main window layout
main_layout = [
    [sg.Text("Please select an option:")],
    [sg.Button("Exit")],
    [sg.Button("RMS List")]
]
rms_list_layout = [
    [sg.Text("Winlink Gateway Utilities")],
    [sg.Button("Update RMS List")],
    [sg.Button("Return to Main")]
]

# Create Windows Here
main_window = sg.Window("N8JJA Radio Utilities", layout=main_layout, margins=(200, 100))
rms_list_window = sg.Window("RMS Gateway List", layout=rms_list_layout, margins=(100, 50))
# Main window event loop
while True:
    event, values = main_window.read()
    # End if user clicks the exit button or closes the window.
    if event == "RMS List":
        event, values = rms_list_window.read()
        if event == "Update RMS List":
            pass
        elif event == "Return to Main":
            rms_list_window.close()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

main_window.close()