import os
import datetime
import webbrowser
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from os import path
from tkinter import *
from qiskit import *
from Tkinter import *
import tkMessageBox

def get_autogen_stat(event=None):
    window2 = Toplevel(window)
    window2.title("Auto Generator Number Statistics")
    window2.geometry("700x750")
    window2.configure(bg="white")
    window2.focus_force()
    photo2 = PhotoImage(file = get_path+'/quantum.png')
    window2.iconphoto(False, photo2)
    window2.bind('<F1>', help)   #add keyboard trigger F1
    try:
        dat_frame = auto_gen.df
    except:
        window2.destroy()
        messagebox.showerror("Error","You need auto generate number before use this tools")
    if(str(varCheck1.get()) == "1"):
        figure = plt.Figure(figsize=(6,6), dpi=110)
        ax = figure.add_subplot(111)
        chart = FigureCanvasTkAgg(figure, window2)
        chart.draw()
        chart.get_tk_widget().place(x=5,y=5)
        dat_frame.plot(x="Number", y="Frequency",kind='bar', legend=True, ax=ax)
        ax.set_title("Frequency distribution among generated random number")
    elif(str(varCheck1.get()) == "2"):
        figure, ax = plt.subplots(figsize=(6,6), dpi=110)
        sns.heatmap(dat_frame, cmap='YlGnBu', annot=True)
        chart = FigureCanvasTkAgg(figure, window2)
        chart.draw()
        chart.get_tk_widget().place(x=5,y=5)
    elif(str(varCheck1.get()) == "3"):
        figure = plt.Figure(figsize=(6,6), dpi=110)
        ax = figure.add_subplot(111)
        chart = FigureCanvasTkAgg(figure, window2)
        chart.draw()
        chart.get_tk_widget().place(x=5,y=5)
        dat_frame.plot(x="Number", y="Frequency",kind='scatter', legend=True, ax=ax, cmap='YlGnBu')
        ax.set_title("Frequency distribution among generated random number")
        

def exports(event=None):
    date = str(datetime.datetime.now()) #get datetime and convert to string
    txt_data = txt_view.get("1.0", END)    #get the data on text_view
    msg_info='''File succesfully opened !!'''   #msg string
    msg_created='''File succesfully created !!'''
    if(not path.exists(get_path+'/Quantum_Random_Number_Output.txt')):  #check if the file is exist
        f=open(get_path+'/Quantum_Random_Number_Output.txt', "xt")  #open the file if the file not exist, create it
        if not f.closed:    #check if the file is still open
            messagebox.showinfo("Info", message=msg_created)    #show messagebox
            f.write(date+"\n"+txt_data) #write the date and text_view
        f.close()   #close file
        webbrowser.open(get_path+'/Quantum_Random_Number_Output.txt')   #auto open the file text using default/prefered text editor
    elif(path.exists(get_path+'/Quantum_Random_Number_Output.txt')):
        f=open(get_path+'/Quantum_Random_Number_Output.txt', "at")
        if not f.closed:
            messagebox.showinfo("Info", message=msg_info)
            f.write(date+"\n"+txt_data)
        f.close()
        webbrowser.open(get_path+'/Quantum_Random_Number_Output.txt')

def auto_gen(event=None):
    f=open(get_path+'/Quantum_Random_Number_Output.txt', "r+")
    f.truncate(0)
    f.seek(0)
    n=int(spin_n.get())
    shot=int(spin_shots.get())
    q=int(spin_qubit.get())
    iteration=int(spin_autogen.get())
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
        if(not path.exists(get_path+'/Quantum_Random_Number_Output.txt')):  #check if the file is exist
                f=open(get_path+'/Quantum_Random_Number_Output.txt', "xt")  #open the file if the file not exist, create it
                if not f.closed:    #check if the file is still open
                    f.write(date+"\n"+txt_data) #write the date and text_view
                f.close()   #close file
        elif(path.exists(get_path+'/Quantum_Random_Number_Output.txt')):
            f=open(get_path+'/Quantum_Random_Number_Output.txt', "at")
        if not f.closed:
            f.write(date+"\n"+txt_data)
        f.close()
    webbrowser.open(get_path+'/Quantum_Random_Number_Output.txt')
    for numbers in rslt_list:
        if numbers in freq:
            freq[numbers] += 1
        else:
            freq[numbers] =1
    auto_gen.df = pd.DataFrame(list(freq.items()), columns=['Number', 'Frequency'])

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
    \nKeyboard Shortcut:
    \t1. Ctrl+g → Generate number
    \t2. Ctrl+c → Clear output from text box
    \t3. Ctrl+e → Export generated data to a file
    \t4. Ctrl+a → Auto Generate random number using how many number iteration given
    \t5. Ctrl+s → See visualization from generated random number
    \t6. F1 → Reopen this window
    \nFor recommended settings click clear button !
    \nAuthor: Felix 'AFÖÉK' Montalfu Ⓚ 2021, All Right Reserved
    '''
    window.option_add('*Dialog.msg.font', 'Calibri 18') #set font for message
    messagebox.showinfo("Help", message=msg)    #show the messagebox
    window.option_clear()   #clear font message

def clear(event=None):
    txt_view.config(state=NORMAL)   #set textbox become NORMAL state
    txt_view.delete(1.0,END)    #delete all text in textbox
    txt_view.config(state=DISABLED) #set textbox become DISABLE state(disable textbox !CANNOT EDIT THE TEXTBOX PROGRAMMATICALLY NOR MANUAL! readonly)
    n_var.set("2")
    shots_var.set("1024")
    qubit_var.set("2")
    auto_gen_var.set("100")

def generate(event=None):
    n = int(spin_n.get())   #get value from spin box
    shot = int(spin_shots.get())
    q = int(spin_qubit.get())
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

#get the path for file
get_path = os.getcwd()
#init all Tkinter UI
window = Tk()
n_var = StringVar(window)
shots_var = StringVar(window)
qubit_var = StringVar(window)
auto_gen_var = StringVar()
var = IntVar(window)
varCheck1 = IntVar(window)
varCheck1.set(1)
var.set(1)
qubit_var.set("1024")
window.geometry("720x365")
photo = PhotoImage(file = get_path+'/quantum.png')
window.iconphoto(False, photo)
window.tk.call('tk','scaling','1')
window.title('Quantum Random Number Generator Simulation UI')
lbl_n = Label(window,text="Iteration: ",justify="left", anchor="e", font=14)
lbl_shots = Label(window, text="Shots: ",justify="left", anchor="e", font=14)
spin_n = Spinbox(window, font=14, from_=1, to=10000, width=6, repeatdelay=200, repeatinterval=90, wrap=True, textvariable=n_var)
spin_shots = Spinbox(window, font=14, width=6, repeatdelay=200, repeatinterval=90, wrap=True ,values=(32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536), textvariable=shots_var)
btn_generate = Button(window, font=14, text="Generate !", padx=10, command=generate, cursor="hand2", underline=0, repeatdelay=200, repeatinterval=90)
txt_view = Text(window, font=14, width=80, wrap=CHAR, xscrollcommand=set())
radio_result = Radiobutton(window, font=14, text="Generate result", value=1, variable = var, underline=9)
radio_binary = Radiobutton(window, font=14, text="Generate binary form", value=2, variable = var, underline=9)
radio_digit = Radiobutton(window, font=14, text="Generate digit", value=3, variable = var, underline=9)
radio_all = Radiobutton(window, font=14, text="Generate all information", value=4, variable = var, underline=9)
lbl_qubit = Label(window, font=14, anchor="e", justify="left", text="Qubit count: ")
spin_qubit = Spinbox(window, font=14, width=6, repeatdelay=100, repeatinterval=90, wrap=True, from_=1, to=5, textvariable=qubit_var)
clr_btn = Button(window, font=14, text="Clear !", padx=10, cursor="hand2", command=clear, underline=0)
export_btn = Button(window, font=14, text="Export !", padx=10, cursor="hand2", command=exports, underline=0)
btn_auto = Button(window, font=5, text="Auto Generate !", padx=5, cursor="hand2", command=auto_gen, underline=0)
lbl_autogen = Label(window, text="Auto Iteration: ", justify="left", anchor="e", font=14)
spin_autogen = Spinbox(window, font=14, from_=1, to=10000, width=6, repeatdelay=200, repeatinterval=90, wrap=True, textvariable=auto_gen_var)
btn_stat = Button(window, font=14, text="Auto Generator Statistics", padx=10, cursor="hand2", command=get_autogen_stat, underline=15)
radio_br = Radiobutton(window, font=14, text="Bar", variable=varCheck1, underline = 0, value = 1)
radio_hm = Radiobutton(window, font=14, text="Heat Map", variable=varCheck1, underline = 0, value = 2)
radio_sc = Radiobutton(window, font=14, text="Scatter Map", variable=varCheck1, underline = 0, value = 3)
#place widget using relative layout
lbl_n.place(x=0, y=5)
spin_n.place(x=70, y=6)
lbl_shots.place(x=0, y=36)
spin_shots.place(x=70, y=38)
btn_generate.place(x=155, y=33)
clr_btn.place(x=265, y=33)
export_btn.place(x=350, y=33)
lbl_qubit.place(x=150, y=5)
spin_qubit.place(x=245, y=6)
radio_result.place(x=0, y=70)
radio_binary.place(x=0, y=93)
radio_digit.place(x=185, y=70)
radio_all.place(x=185, y=93)
lbl_autogen.place(x=325, y=5)
spin_autogen.place(x=430, y=6)
txt_view.place(x=0, y=125)
btn_auto.place(x=440, y=33)
btn_stat.place(x=380, y=70)
radio_br.place(x=595, y=6)
radio_hm.place(x=595, y=33)
radio_sc.place(x=595, y=59)
#Keyboard bind
window.bind('<F1>', help)   #add keyboard trigger F1
window.bind('<Control_L><g>', generate) #add keyboard trigger Ctrl+g
window.bind('<Control_L><c>', clear)    #add keyboard trigger Ctrl+c
window.bind('<Control_L><e>', exports)  #add keyboard trigger Ctrl+e
window.bind('<Control_L><a>', auto_gen) #add keyboard trigger Ctrl+a
window.bind('<Control_L><s>', get_autogen_stat) #add keyboard trigger Ctrl+s
help()
window.mainloop()