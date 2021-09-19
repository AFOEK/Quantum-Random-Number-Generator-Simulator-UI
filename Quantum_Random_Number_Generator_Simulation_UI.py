import os
import datetime
import webbrowser
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from os import path
from tkinter import *
from tkinter import messagebox
from qiskit import *
from tkinter import font as Font
from qiskit.algorithms import Shor
from qiskit.utils import QuantumInstance
from re import search
from numpy import *
import numpy as py
from math import gcd
from qiskit.providers.aer import AerError

__version__ = "0.2.3rc4"

def get_autogen_stat(event=None):
    window2 = Toplevel(window)
    window2.title("Auto Generator Number Statistics")
    window2.geometry("700x750")
    window2.configure(bg="white")
    window2.focus_force()
    photo2 = PhotoImage(file = get_path+'/quantum.png')
    window2.iconphoto(False, photo2)
    window2.bind('<F1>', help)   #add keyboard trigger F1
    #Check if dataframe is exist
    try:
        dat_frame = auto_gen.df
    except:     #handling empty datafrane
        window2.destroy()
        messagebox.showerror("Error","You need auto generate number before use this tools")
    if(str(varCheck1.get()) == "1"):    #check if option bar char is checked
        figure = plt.Figure(figsize=(6,6), dpi=110) #init figure for matplotlib
        ax = figure.add_subplot(111)    #add new sub plot
        chart = FigureCanvasTkAgg(figure, window2)  #create new canvas above Tkinter window
        chart.draw()    #draw the chart
        chart.get_tk_widget().place(x=5,y=5)    #place chart in Tkinter widget
        dat_frame.plot(x="Number", y="Frequency",kind='bar', legend=True, ax=ax) #plot the data to bar chart with legend and info
        ax.set_title("Frequency distribution among generated random number")    #set plot title
    elif(str(varCheck1.get()) == "2"):
        figure, ax = plt.subplots(figsize=(6,6), dpi=110)
        sns.heatmap(dat_frame, cmap='YlGnBu', annot=True)   #make new seaborn heatmap using Yelllow, Green, and Blue color map
        chart = FigureCanvasTkAgg(figure, window2)
        chart.draw()
        chart.get_tk_widget().place(x=5,y=5)
    elif(str(varCheck1.get()) == "3"):
        figure = plt.Figure(figsize=(6,6), dpi=110)
        ax = figure.add_subplot(111)
        chart = FigureCanvasTkAgg(figure, window2)
        chart.draw()
        chart.get_tk_widget().place(x=5,y=5)
        dat_frame.plot(x="Number", y="Frequency",kind='scatter', legend=True, ax=ax, cmap='YlGnBu') #plot the data to scatter chart with legend and info
        ax.set_title("Frequency distribution among generated random number")
        

def exports(event=None):
    date = str(datetime.datetime.now()) #get datetime and convert to string
    txt_data = txt_view.get("1.0", END)    #get the data on text_view
    if txt_data == "\n":    #check if text box are enter (default value)
        messagebox.showerror(title="ERROR", message="You need generate number first !") #GUI error msg
    else:
        msg_info='''File succesfully opened !!'''   #msg string
        msg_created='''File succesfully created !!'''
        if(not path.exists(get_path+'/shor.flog')):  #check if the file is exist
            f=open(get_path+'/shor.flog', "xt")  #open the file if the file not exist, create it
            if not f.closed:    #check if the file is still open
                messagebox.showinfo("Info", message=msg_created)    #show messagebox
                f.write(date+"\n"+txt_data) #write the date and text_view
            f.close()   #close file
            webbrowser.open(get_path+'/shor.flog')   #auto open the file text using default/prefered text editor
        elif(path.exists(get_path+'/shor.flog')):
            f=open(get_path+'/shor.flog', "at")
            if not f.closed:
                messagebox.showinfo("Info", message=msg_info)
                f.write(date+"\n"+txt_data)
            f.close()
            webbrowser.open(get_path+'/shor.flog')
    

def auto_gen(event=None):
    f=open(get_path+'/shor.flog', "r+")  #open the file using read mode with pointer set to beginning of file
    f.truncate(0)   #Clear the file content
    f.seek(0)   #set pointer to beginning of file
    n=int(spin_n.get()) #get number of loop
    shot=int(spin_shots.get())  #get number of shot
    q=int(spin_qubit.get()) #get number of qubit
    backend = option_var.get()  #get the backend
    iteration=int(spin_autogen.get())   #get number of iteration
    rslt_list = []  
    freq = {}
    for j in range (0, iteration):
        circ = QuantumCircuit(q,q)  #init quantum circuit
        if(q==1):
            for i in range(0,q):
                circ.h(i)   #add H-gate
                circ.measure(i,i)
        elif(q==2):
            for i in range(0,q):
                circ.h(i)
                circ.measure(i,i)
        elif(q==3):
            for i in range(0,q):
                circ.h(i)
                circ.measure(i,i)
        elif(q==4):
            for i in range(0,q):
                circ.h(i)
                circ.measure(i,i)
        elif(q==5):
            for i in range(0,q):
                circ.h(i)
                circ.measure(i,i)
        number = [] #init a list  
        for i in range(0,int(n)):   #how many iteration which effect how many digit created
            if(search("gpu", backend)):
                try:
                    sim = Aer.get_backend(backend.replace('_gpu',''))
                    sim.set_options(device='GPU')
                except AerError:
                    pass
            else:
                sim = Aer.get_backend(backend) #get qiskit simulator
            job = execute(circ, sim, shots = int(shot))   #execute job using existing circuit, simulator, and number of shot
            result = job.result()   #get the job result
            count = result.get_counts(circ) #get the probability count datatype→dict
            max_prob = max(count, key=count.get)    #get the highest probability from the count
            number.append(max_prob) #append all generated number to list
        strings = [str(number) for number in number]    #convert all number in list become a list string
        bit_string = "".join(strings)   #convert list string become bitstring
        rslt = int(bit_string,2)    #convert all bitstring become integer
        digit = str(len(str(rslt))) #count lenght of result
        rslt_list.append(rslt)
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
        date = str(datetime.datetime.now()) #get datetime and convert to string
        txt_data = txt_view.get("1.0", END)    #get the data on text_view
        if(not path.exists(get_path+'/shor.flog')):  #check if the file is exist
                f=open(get_path+'/shor.flog', "xt")  #open the file if the file not exist, create it
                if not f.closed:    #check if the file is still open
                    f.write(date+"\n"+txt_data) #write the date and text_view
                f.close()   #close file
        elif(path.exists(get_path+'/shor.flog')):
            f=open(get_path+'/shor.flog', "at")
        if not f.closed:
            f.write(date+"\n"+txt_data)
        f.close()
    webbrowser.open(get_path+'/shor.flog')
    for numbers in rslt_list:
        if numbers in freq:
            freq[numbers] += 1
        else:
            freq[numbers] =1
    auto_gen.df = pd.DataFrame(list(freq.items()), columns=['Number', 'Frequency'])
    circ.draw(output="mpl", filename="circuit_output\\qrng_circuit.png")
    circ.draw(output="latex", filename="circuit_output\\qrng_circuit_latex.png")
    circ.draw(output="latex_source", filename="circuit_output\\qrng_circuit_tex.tex")
    circ.draw(output="text", filename="circuit_output\\qrng_circuit_tex.txt")

def help(event=None):
    msg = '''Iteration → It's for generate how many digits and it's depends how many qubits you give with formula: 2^n with n (how many qubit allocated)
    \nShots → It's make your generated random number more accurate and more diverse
    \nQubit Count → It's for how many bit string generated which will be safe into array list
    \nGenerate result → It'll generate an integer number
    \nGenerate binary → It'll generate a binary form
    \nGenerate digit → It'll count how many digit from an integer
    \nClear → It'll clear all data from textbox
    \nGenerate all information → It'll generate all information such as integer, digit, and binary form
    \nExport → It'll export output from text box to an file
    \nAuto generate → It'll generate output and export it into a file
    \nAuto generate statistic → It'll create visualization using bar, heatmap, or line graph
    \nBackend → It'll use backend what you choose
    \nKeyboard Shortcut:
    \t1. Ctrl+g → Generate number
    \t2. Ctrl+c → Clear output from text box
    \t3. Ctrl+e → Export generated data to a file
    \t4. Ctrl+a → Auto Generate random number using how many number iteration given
    \t5. Ctrl+s → See visualization from generated random number
    \t6. Ctrl+Shift+b → Select bar chart
    \t7. Ctrl+Shift+h → Select heatmap
    \t8. Ctrl+Shift+s → Select scattermap
    \t9. Ctrl+r → Select Result
    \t10. Ctrl+b → Select Binary
    \t11. Ctrl+d → Select Digit
    \t12. Crtl+Shift+A → Select All Information
    \t13. F1 → Reopen this window
    \nFor recommended settings click clear button !
    \nAuthor: Felix 'AFÖÉK' Montalfu Ⓚ 2021, All Right Reserved
    \nGithub link: https://github.com/AFOEK/Quantum-Random-Number-Generator-Simulator-UI
    '''
    messagebox.showinfo("Help", message=msg)    #show the messagebox
    window.option_clear()   #clear font message

def clear(event=None):
    txt_view.config(state=NORMAL)   #set textbox become NORMAL state
    txt_view.delete(1.0,END)    #delete all text in textbox
    txt_view.config(state=DISABLED) #set textbox become DISABLE state(disable textbox !CANNOT EDIT THE TEXTBOX PROGRAMMATICALLY NOR MANUAL! readonly)
    #set all var to assigned value
    n_var.set("2")
    shots_var.set("1024")
    qubit_var.set("2")
    auto_gen_var.set("100")

def generate(event=None):
    n = int(spin_n.get())   #get value from spin box
    shot = int(spin_shots.get())
    q = int(spin_qubit.get())
    backend = option_var.get()
    circ = QuantumCircuit(q,q)  #init quantum circuit
    if(q==1):
        for i in range(0,q):
            circ.h(i)   #add H-gate
            circ.measure(i,i)
    elif(q==2):
        for i in range(0,q):
            circ.h(i)
            circ.measure(i,i)
    elif(q==3):
        for i in range(0,q):
            circ.h(i)
            circ.measure(i,i)
    elif(q==4):
        for i in range(0,q):
            circ.h(i)
            circ.measure(i,i)
    elif(q==5):
        for i in range(0,q):
            circ.h(i)
            circ.measure(i,i)
    number = [] #init a list  
    for i in range(0,int(n)):   #how many iteration which effect how many digit created
        if(search("gpu", backend)):
            try:
                sim = Aer.get_backend(backend.replace('_gpu',''))
                sim.set_options(device='GPU')
            except AerError:
                pass
        else:
            sim = Aer.get_backend(backend) #get qiskit simulator
        job = execute(circ, sim, shots = int(shot))   #execute job using existing circuit, simulator, and number of shot
        result = job.result()   #get the job result
        count = result.get_counts(circ) #get the state probability count datatype→dict
        max_prob = max(count, key=count.get)    #get the highest probability from the count
        number.append(max_prob) #append all generated number to list
    strings = [str(number) for number in number]    #convert all number in list become a list string
    generate.bit_string = "".join(strings)   #convert list string become bitstring
    generate.rslt = int(generate.bit_string,2)    #convert all bitstring become integer
    generate.digit = str(len(str(generate.rslt))) #count lenght of result
    if(str(var.get()) == "1"):  #get value of radio button
        txt_view.config(state=NORMAL)   #enable textbox
        txt_view.delete(1.0,END)    #clear all entry
        txt_view.insert(INSERT, str(generate.rslt))  #insert the result
        txt_view.config(state=DISABLED) #disable or readonly mode
    elif(str(var.get()) == "2"):
        txt_view.config(state=NORMAL)
        txt_view.delete(1.0,END)
        txt_view.insert(INSERT, generate.bit_string)
        txt_view.config(state=DISABLED)
    elif(str(var.get()) == "3"):
        txt_view.config(state=NORMAL)
        txt_view.delete(1.0,END)
        txt_view.insert(INSERT, str(generate.digit))
        txt_view.config(state=DISABLED)
    elif(str(var.get()) == "4"):
        txt_view.config(state=NORMAL)
        txt_view.delete(1.0,END)
        txt_view.insert(INSERT, str(generate.digit) +"\n" + str(generate.rslt) +"\n"+ str(generate.bit_string))
        txt_view.config(state=DISABLED)
    circ.draw(output="mpl", filename="circuit_output\\qrng_circuit.png")
    circ.draw(output="latex", filename="circuit_output\\qrng_circuit_latex.png")
    circ.draw(output="latex_source", filename="circuit_output\\qrng_circuit_tex.tex")
    circ.draw(output="text", filename="circuit_output\\qrng_circuit_tex.txt")

def select_bar(event=None):
    varCheck1.set(1)

def select_heatmap(event=None):
    varCheck1.set(2)

def select_scatter(event=None):
    varCheck1.set(3)

def select_result(event=None):
    var.set(1)

def select_bin(event=None):
    var.set(2)

def select_digit(event=None):
    var.set(3)

def select_all(event=None):
    var.set(4)

def factorize(event=None):
    #init window and config
    window3 = Toplevel(window)
    window3.title("Factorize")
    window3.geometry("350x50")
    window3.configure(bg="white")
    window3.focus_force()
    photo3 = PhotoImage(file = get_path+'/quantum.png')
    window3.iconphoto(False, photo3)
    lbl_var = StringVar()
    #Label init
    lbl_rslt = Label(window3, text="",font=25, justify="left", anchor="e", textvariable=lbl_var, bg="white")
    #place widget using relative layout
    lbl_rslt.place(x=3, y=3)
    #try if the generate result is not empty and successfully created
    try:
        result = generate.rslt
    except:
        window3.destroy()
        messagebox.showerror("Error","You need generate a number before use this tools")
    shot = int(spin_shots.get())
    backend = option_var.get()
    if(search("gpu", backend)): #serach if backend string contain "_gpu"
        try:
            sim = Aer.get_backend(backend.replace('_gpu',''))   #set the backend without "_gpu" because qiskit doesn't have that backend name
            sim.set_options(device='GPU')   #set simulator option to run using Nvidia GPU
            window3.focus_force()   #re-focus windows
        except AerError as e:   #Get error from Aer simulator
            messagebox.showerror("Error","Your device doesn't have Nvidia GPU or CUDA installed \nplease check again if your CUDA is installed correctly")  #warn user if their device doesn't have GPU or CUDA
            pass    #just do other code, don't stop
    else:
        sim = Aer.get_backend(backend) #get qiskit simulator
    #init quantum instance and Shor's algorithm
    quantum_instance = QuantumInstance(sim, shots=shot) #create a QuantumInstance
    shor = Shor(quantum_instance=quantum_instance)  #Create Shor circuit using previous QuantumInstance
    rslt = shor.factor(result)  #get the result factor
    final_rslt = rslt.factors[0]    #get the first list of the result
    lbl_var.set("Result factor of " + str(result) + " is " + str(final_rslt))   #set the result to existing label
    date = str(datetime.datetime.now())
    if(not path.exists(get_path+'/shor.flog')):  #check if the file is exist
        f=open(get_path+'/shor.flog', "xt")  #open the file if the file not exist, create it
        if not f.closed:    #check if the file is still open
            f.write(date+"\n"+str(rslt)) #write the date and result
        f.close()   #close file
    elif(path.exists(get_path+'/shor.flog')):
        f=open(get_path+'/shor.flog', "at")
    if not f.closed:
        f.write(date+"\n"+str(rslt))
    f.close()
    shor.construct_circuit(rslt).draw(output="mpl", filename="circuit_output\\shor_circuit.png")
    shor.construct_circuit(rslt).draw(output="latex", filename="circuit_output\\shor_circuit.png")
    shor.construct_circuit(rslt).draw(output="latex_source", filename="circuit_output\\shor_circuit.tex")
    shor.construct_circuit(rslt).draw(output="text", filename="circuit_output\\shor_circuit.txt")

#main  program
#get the path for file
get_path = os.getcwd()
#Set option value for drop down menu
options = [
    'aer_simulator',
    'qasm_simulator',
    'statevector_simulator',
    'aer_simulator_stabilizer',
    'aer_simulator_statevector',
    'aer_simulator_density_matrix',
    'aer_simulator_matrix_product_state',
    'aer_simulator_gpu',
    'qasm_simulator_gpu',
    'statevector_simulator_gpu',
    'aer_simulator_statevector_gpu',
    'aer_simulator_density_matrix_gpu',
    'aer_simulator_matrix_product_state_gpu',
]
#init all Tkinter UI and Settings
window = Tk()
window.configure(bg="white")
n_var = StringVar(window)
shots_var = StringVar(window)
qubit_var = StringVar(window)
auto_gen_var = StringVar(window)
option_var = StringVar(window)
var = IntVar(window)
varCheck1 = IntVar(window)
varCheck1.set(1)
var.set(1)
option_var.set(options[0])
qubit_var.set("1024")
window.geometry("950x365")
photo = PhotoImage(file = get_path+'/quantum.png')
window.iconphoto(False, photo)
window.tk.call('tk','scaling','1')
window.title('Quantum Random Number Generator Simulation UI')
font14 = Font.Font(size=10)
font11 = Font.Font(size=11)
#Label init
lbl_n = Label(window,text="Iteration: ",justify="left", anchor="e", font=14, bg="white")
lbl_shots = Label(window, text="Shots: ",justify="left", anchor="e", font=14, bg="white")
lbl_qubit = Label(window, text="Qubit count: ", font=14, anchor="e", justify="left", bg="white")
lbl_autogen = Label(window, text="Auto Iteration: ", justify="left", anchor="e", font=14, bg="white")
lbl_backend = Label(window, text="Backend: ", font=14, justify="left", anchor="e", bg="white")
#Spinbox init
spin_n = Spinbox(window, font=14, from_=1, to=10000, width=6, repeatdelay=200, repeatinterval=90, wrap=True, textvariable=n_var,bg="white")
spin_qubit = Spinbox(window, font=14, width=6, repeatdelay=100, repeatinterval=90, wrap=True, from_=1, to=5, textvariable=qubit_var,bg="white")
spin_shots = Spinbox(window, font=14, width=6, repeatdelay=200, repeatinterval=90, wrap=True ,values=(32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536), textvariable=shots_var,bg="white")
spin_autogen = Spinbox(window, font=14, from_=1, to=10000, width=6, repeatdelay=200, repeatinterval=90, wrap=True, textvariable=auto_gen_var,bg="white")
#Button init
btn_clear = Button(window, font=14, text="Clear !", padx=10, cursor="hand2", command=clear, underline=0,bg="white")
btn_export = Button(window, font=14, text="Export !", padx=10, cursor="hand2", command=exports, underline=0,bg="white")
btn_auto = Button(window, font=5, text="Auto Generate !", padx=5, cursor="hand2", command=auto_gen, underline=0,bg="white")
btn_generate = Button(window, font=14, text="Generate !", padx=10, command=generate, cursor="hand2", underline=0, repeatdelay=200, repeatinterval=90,bg="white")
btn_stat = Button(window, font=14, text="Auto Generator Statistics", padx=10, cursor="hand2", command=get_autogen_stat, underline=15,bg="white")
btn_shors = Button(window, font=14, text="Factorize", padx=5, command=factorize, cursor="hand2", underline=0,bg="white")
#Text init
txt_view = Text(window, font=14, width=94, wrap=CHAR, xscrollcommand=set(), bg="white")
#Drop menu init
drop_menu = OptionMenu(window, option_var, *options)
drop_menu.config(font=font14)
option_menu = window.nametowidget(drop_menu.menuname)
option_menu.config(font=font11)
#Radio init
radio_result = Radiobutton(window, font=14, text="Generate result", value=1, variable = var, underline=9, bg="white")
radio_binary = Radiobutton(window, font=14, text="Generate binary form", value=2, variable = var, underline=9, bg="white")
radio_digit = Radiobutton(window, font=14, text="Generate digit", value=3, variable = var, underline=9, bg="white")
radio_all = Radiobutton(window, font=14, text="Generate all information", value=4, variable = var, underline=9, bg="white")
radio_br = Radiobutton(window, font=14, text="Bar", variable=varCheck1, underline = 0, value = 1, bg="white")
radio_hm = Radiobutton(window, font=14, text="Heat Map", variable=varCheck1, underline = 0, value = 2, bg="white")
radio_sc = Radiobutton(window, font=14, text="Scatter Map", variable=varCheck1, underline = 0, value = 3, bg="white")
#place widget using relative layout
lbl_n.place(x=0, y=5)
spin_n.place(x=70, y=6)
lbl_shots.place(x=0, y=36)
spin_shots.place(x=70, y=38)
btn_generate.place(x=155, y=33)
btn_clear.place(x=270, y=33)
btn_export.place(x=350, y=33)
lbl_qubit.place(x=150, y=5)
spin_qubit.place(x=245, y=6)
radio_result.place(x=0, y=70)
radio_binary.place(x=0, y=93)
radio_digit.place(x=215, y=70)
radio_all.place(x=215, y=93)
lbl_autogen.place(x=325, y=5)
spin_autogen.place(x=445, y=6)
txt_view.place(x=0, y=125)
btn_auto.place(x=440, y=33)
btn_stat.place(x=465, y=70)
radio_br.place(x=698, y=35)
radio_hm.place(x=698, y=57)
radio_sc.place(x=698, y=79)
lbl_backend.place(x=534, y=5)
drop_menu.place(x=614, y=3)
btn_shors.place(x=745, y=3)
#Keyboard bind
window.bind('<F1>', help)   #add keyboard trigger F1
window.bind('<Control_L><g>', generate) #add keyboard trigger Ctrl+g
window.bind('<Control_L><c>', clear)    #add keyboard trigger Ctrl+c
window.bind('<Control_L><e>', exports)  #add keyboard trigger Ctrl+e
window.bind('<Control_L><a>', auto_gen) #add keyboard trigger Ctrl+a
window.bind('<Control_L><s>', get_autogen_stat) #add keyboard trigger Ctrl+s
window.bind('<Control_L><B>', select_bar)   #add keyboard trigger Ctrl+Shift+b
window.bind('<Control_L><H>', select_heatmap)   #add keyboard trigger Ctrl+Shift+h
window.bind('<Control_L><S>', select_scatter)   #add keyboard trigger Ctrl+Shift+s
window.bind('<Control_L><r>', select_result)    #add keyboard trigger Ctrl+r
window.bind('<Control_L><b>', select_bin)   #add keyboard trigger Ctrl+b
window.bind('<Control_L><d>', select_digit) #add keyboard trigger Ctrl+d
window.bind('<Control_L><A>', select_all)   #add keyboard trigger Ctrl+Shift+A
window.bind('<Control_L><f>', factorize)    #add keyboard trigger Ctrl+f
help()
window.mainloop()