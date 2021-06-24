import tkinter as tk
from tkinter import *
from math import *
from qiskit import *
import qiskit as q

def generate():
    n = int(spin_n.get())
    shot = int(spin_shots.get())
    circ = QuantumCircuit(2,2)
    circ.h(0)
    circ.cx(0,1)
    circ.measure(0,0)
    circ.measure(1,1)
    number =[]
    for i in range(0,int(n)):
        sim = Aer.get_backend('qasm_simulator')
        job = q.execute(circ, sim, shots = int(shot))
        result = job.result()
        count = result.get_counts(circ)
        max_prob = max(count, key=count.get)
        number.append(max_prob)
    strings = [str(number) for number in number]
    bit_string = "".join(strings)
    rslt = int(bit_string,2)
    digit = str(len(str(rslt)))
    if(str(var.get()) == "1"):
        txt_view.insert(INSERT, str(rslt))
    elif(str(var.get()) == "2"):
        txt_view.insert(INSERT, bit_string)
    elif(str(var.get()) == "3"):
        txt_view.insert(INSERT, str(digit))
    elif(str(var.get()) == "4"):
        txt_view.insert(INSERT, str(digit) +"\n" + str(rslt) +"\n"+ str(bit_string))

window = tk.Tk()
var = IntVar()
window.geometry("450x355+450+355")
photo = PhotoImage(file = 'quantum.png')
window.iconphoto(False, photo)
window.title('Quantum Random Number Generator Simulation UI')
lbl_n = Label(window,text="Iteration: ",justify="left", anchor="e",font=14)
lbl_shots = Label(window, text="Shots: ",justify="left", anchor="e",font=14)
spin_n = Spinbox(window, font=14, from_=1, to=10000, width=6, repeatdelay=200, repeatinterval=90, wrap=True)
spin_shots = Spinbox(window, font=14, width=6, repeatdelay=200, repeatinterval=90, wrap=True ,values=(32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536))
btn_generate = Button(window, font=14, text="Generate !", padx=10, command=generate, cursor="hand2")
txt_view = Text(window, font=14, width=50, wrap=CHAR, xscrollcommand=set())
radio_result = Radiobutton(window, font=14, text="Generate result", value=1, variable = var)
radio_binary = Radiobutton(window, font=14, text="Generate binary form", value=2, variable = var)
radio_digit = Radiobutton(window, font=14, text="Generate digit", value=3, variable = var)
radio_all = Radiobutton(window, font=14, text="Generate all information", value=4, variable = var)
#place widget using relative layout
lbl_n.place(x=0, y=5)
spin_n.place(x=70, y=6)
lbl_shots.place(x=0, y=36)
spin_shots.place(x=70, y=38)
btn_generate.place(x=150, y=16)
radio_result.place(x=0, y=65)
radio_binary.place(x=0, y=85)
radio_digit.place(x=185, y=65)
radio_all.place(x=185, y=85)
txt_view.place(x=0, y=120)
window.mainloop()