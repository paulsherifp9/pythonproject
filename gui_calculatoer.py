import tkinter as tk

window = tk.Tk()

window.title("GUI Calculator")

window.geometry("300x400")
entry = tk.Entry(
    window,
    width=20,
    font=("Arial", 20),
    borderwidth=5,
    justify="right"
)

entry.pack(pady=20)
def click(number):

    current = entry.get()

    entry.delete(0, tk.END)

    entry.insert(0, current + str(number))
    
def clear():

    entry.delete(0, tk.END)
def equal():

    expression = entry.get()

    result = eval(expression)

    entry.delete(0, tk.END)

    entry.insert(0, str(result))

button_1 = tk.Button(window, text="1", padx=20, pady=20,
                     command=lambda: click(1))

button_2 = tk.Button(window, text="2", padx=20, pady=20,
                     command=lambda: click(2))

button_3 = tk.Button(window, text="3", padx=20, pady=20,
                     command=lambda: click(3))

button_add = tk.Button(window, text="+", padx=20, pady=20,
                       command=lambda: click("+"))

button_equal = tk.Button(window, text="=", padx=20, pady=20,
                         command=equal)

button_clear = tk.Button(window, text="C", padx=20, pady=20,
                         command=clear)
button_1.pack()
button_2.pack()
button_3.pack()
button_add.pack()
button_equal.pack()
button_clear.pack()
window.mainloop()