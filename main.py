import tkinter

# Create Main Window
mainWindow = tkinter.Tk()
mainWindow.geometry("1280x720")
mainWindow.title("Timetabling Helper Program")

titleLable = tkinter.Label(mainWindow, text="Yes.... this needs a lot of work!")
titleLable.grid(row=0, column=0, columnspan=4, sticky='ew')

quitButton = tkinter.Button(mainWindow, text="Quit", command=mainWindow.destroy)
quitButton.grid(row=5, column=4, sticky='nw')

mainWindow.mainloop()