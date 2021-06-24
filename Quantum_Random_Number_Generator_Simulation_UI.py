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

window = tk.Tk()
window.geometry("350x345+350+345")
window.title('Quantum Random Number Generator Simulation UI')
lbl_n = Label(window,text="Iteration: ",justify="left", anchor="e",font=14)
lbl_shots = Label(window, text="Shots: ",justify="left", anchor="e",font=14)
spin_n = Spinbox(window, font=14, from_=0, to=10000, width=6, repeatdelay=200, repeatinterval=90, wrap=True)
spin_shots = Spinbox(window, font=14, width=6, repeatdelay=200, repeatinterval=90, wrap=True ,values=(32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536))
btn_generate = Button(window, font=14, text="Generate !", padx=10, command=generate, cursor="hand2")
txt_view = Text(window, font=14, padx=10, wrap=CHAR, xscrollcommand=set())
lbl_n.place(x=0, y=5)
spin_n.place(x=70, y=6)
lbl_shots.place(x=0, y=36)
spin_shots.place(x=70, y=38)
btn_generate.place(x=150, y=16)
#txt_view.pack()
window.mainloop()