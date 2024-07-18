import tkinter as tk

def on_button_click():
    label.config(text="Hola, presionaste el botón")

root = tk.Tk()
root.title("Mi aplicación de ventana")

label = tk.Label(root, text="Bienvenido a mi aplicación de ventana")
label.pack()

button = tk.Button(root, text="Presionar", command=on_button_click)
button.pack()

root.mainloop()