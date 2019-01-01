import tkinter as tk

app = tk.Tk()

list_b = tk.Listbox(app, width=100)
list_b.pack()

for each in ['Hello!', 'sdfasdfsadfasdf', 'fnasuiodfhasduiofhsad']:
    list_b.insert(tk.END, str(each))

tk.mainloop()
