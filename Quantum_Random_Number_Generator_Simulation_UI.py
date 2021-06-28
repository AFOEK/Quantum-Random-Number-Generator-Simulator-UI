import tkinter as tk
from tkinter import Text, Button, PhotoImage, Radiobutton, Tk, Spinbox, IntVar, Label, CHAR, NORMAL, END, DISABLED, INSERT, messagebox
from qiskit import Aer, QuantumCircuit, QuantumRegister, execute

def help(event = None):
    msg = '''Iteration → It's for generate how many digits and it's depends how many qubits you give with formula: 2^n with n (how many qubit allocated)
    \n\nShots → It's make your generated random number more accurate and more diverse
    \n\nQubit Count → It's for how many bit string generated which will be safe into array list
    \n\nGenerate result → It'll generate an integer number
    \n\nGenerate binary → It'll generate a binary form
    \n\nGenerate digit → It'll count how many digit from an integer
    \n\nGenerate all information → it'll generate all information such as integer, digit, and binary form
    '''
    window.option_add('*Dialog.msg.font', 'Calibri 18') #set font for message
    messagebox.showinfo("Help", message=msg)
    window.option_clear()   #clear font message

def clear():
    txt_view.config(state=NORMAL)   #set textbox become NORMAL state
    txt_view.delete(1.0,END)    #delete all text in textbox
    txt_view.config(state=DISABLED) #set textbox become DISABLE state(disable textbox !CANNOT EDIT THE TEXTBOX PROGRAMMATICALLY NOR MANUAL! readonly mode)

def generate():
    n = int(spin_n.get())   #get value from spin box
    shot = int(spin_shots.get())
    q = int(spin_qubit.get())
    circ = QuantumCircuit(q,q)  #init quantum circuit
    if(q==1):
        circ.h(0)   #add hadamard gate to first wire
        circ.measure(0,0)   #add measurement first wire to first classical output
    elif(q==2):
        circ.h(0)   #add hadamard gate to first wire
        circ.h(1)   #add hadamard gate to second wire
        circ.measure(0,0)   #add measurement first wire to first classical output
        circ.measure(1,1)   #add measurement second wire to second classical output
    elif(q==3):
        circ.h(0)   #add hadamard gate to first wire
        circ.h(1)   #add hadamard gate to second wire
        circ.h(2)   #add hadamard gate to third wire
        circ.measure(0,0)   #add measurement first wire to first classical output
        circ.measure(1,1)   #add measurement second wire to second classical output
        circ.measure(2,2)   #add measurement third wire to third classical output
    elif(q==4):
        circ.h(0)   #add hadamard gate to first wire
        circ.h(1)   #add hadamard gate to second wire
        circ.h(2)   #add hadamard gate to third wire
        circ.h(3)   #add hadamard gate to fourth wire
        circ.measure(0,0)   #add measurement first wire to first classical output
        circ.measure(1,1)   #add measurement second wire to second classical output
        circ.measure(2,2)   #add measurement third wire to third classical output
        circ.measure(3,3)   #add measurement forth wire to forth classical output
    elif(q==5):
        circ.h(0)   #add hadamard gate to first wire
        circ.h(1)   #add hadamard gate to second wire
        circ.h(2)   #add hadamard gate to third wire
        circ.h(3)   #add hadamard gate to fourth wire
        circ.h(4)   #add hadamard gate to fifth wire
        circ.measure(0,0)   #add measurement first wire to first classical output
        circ.measure(1,1)   #add measurement second wire to second classical output
        circ.measure(2,2)   #add measurement third wire to third classical output
        circ.measure(3,3)   #add measurement forth wire to forth classical output
        circ.measure(4,4)   #add measurement fifth wire to fifth classical output
    number = [] #init a list  
    for i in range(0,int(n)):   #how many iteration which effect how many digit created
        sim = Aer.get_backend('qasm_simulator') #get qiskit simulator
        job = execute(circ, sim, shots = int(shot))   #execute job using existing circuit, simulator, and number of shot
        result = job.result()   #get the job result
        count = result.get_counts(circ) #get the probability count datatype→dict
        max_prob = max(count, key=count.get)    #get the highest probability from the count
        number.append(max_prob) #append all generated number to list
    strings = [str(number) for number in number]    #convert all number in list become a list string
    bit_string = "".join(strings)   #convert list string become bitstring
    rslt = int(bit_string,2)    #convert all bitstring become integer
    digit = str(len(str(rslt))) #count lenght of result
    if(str(var.get()) == "1"):  #get value of radio button
        txt_view.config(state=NORMAL)   #enable textbox
        txt_view.delete(1.0,END)    #clear all entry
        txt_view.insert(INSERT, str(rslt))  #insert the result
        txt_view.config(state=DISABLED) #disable or readonly mode
    elif(str(var.get()) == "2"):
        txt_view.config(state=NORMAL)
        txt_view.delete(1.0,END)
        txt_view.insert(INSERT, bit_string)
        txt_view.config(state=DISABLED)
    elif(str(var.get()) == "3"):
        txt_view.config(state=NORMAL)
        txt_view.delete(1.0,END)
        txt_view.insert(INSERT, str(digit))
        txt_view.config(state=DISABLED)
    elif(str(var.get()) == "4"):
        txt_view.config(state=NORMAL)
        txt_view.delete(1.0,END)
        txt_view.insert(INSERT, str(digit) +"\n" + str(rslt) +"\n"+ str(bit_string))
        txt_view.config(state=DISABLED)
#init all Tkinter UI
window = Tk()
var = IntVar()
var.set(1)
window.geometry("495x365+495+365")
photo = PhotoImage(file = 'quantum.png')
window.iconphoto(False, photo)
window.title('Quantum Random Number Generator Simulation UI')
lbl_n = Label(window,text="Iteration: ",justify="left", anchor="e",font=14)
lbl_shots = Label(window, text="Shots: ",justify="left", anchor="e",font=14)
spin_n = Spinbox(window, font=14, from_=1, to=10000, width=6, repeatdelay=200, repeatinterval=90, wrap=True)
spin_shots = Spinbox(window, font=14, width=6, repeatdelay=200, repeatinterval=90, wrap=True ,values=(32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536))
btn_generate = Button(window, font=14, text="Generate !", padx=10, command=generate, cursor="hand2")
txt_view = Text(window, font=14, width=55, wrap=CHAR, xscrollcommand=set())
radio_result = Radiobutton(window, font=14, text="Generate result", value=1, variable = var, underline=9)
radio_binary = Radiobutton(window, font=14, text="Generate binary form", value=2, variable = var, underline=9)
radio_digit = Radiobutton(window, font=14, text="Generate digit", value=3, variable = var, underline=9)
radio_all = Radiobutton(window, font=14, text="Generate all information", value=4, variable = var, underline=9)
lbl_qubit = Label(window, font=14, anchor="e", justify="left", text="Qubit count: ")
spin_qubit = Spinbox(window, font=14, width=6, repeatdelay=100, repeatinterval=90, wrap=True, from_=1, to=5)
clr_btn = Button(window, font=14, text="Clear !", padx=10, cursor="hand2", command=clear)
#place widget using relative layout
lbl_n.place(x=0, y=5)
spin_n.place(x=70, y=6)
lbl_shots.place(x=0, y=36)
spin_shots.place(x=70, y=38)
btn_generate.place(x=155, y=33)
clr_btn.place(x=265, y=33)
lbl_qubit.place(x=150, y=5)
spin_qubit.place(x=245, y=6)
radio_result.place(x=0, y=70)
radio_binary.place(x=0, y=93)
radio_digit.place(x=185, y=70)
radio_all.place(x=185, y=93)
txt_view.place(x=0, y=125)
#Keyboard bind
window.bind('<F1>', help)
window.mainloop()