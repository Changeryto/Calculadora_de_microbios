import tkinter as tk
from tkinter import ttk
from calculos import Calculos
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser



# Validadores

def entero(text):
    if text in "0123456789":
        try:
            int(text)
            return True
        except ValueError:
            return False
    else:
        return False
            

def realp(text):
    if text == "":
        return True
    
    elif text.startswith("E"):
        return False
    
    elif text.endswith("E"):
        if len(text.split("E"))-1 < 2:
            return True
        else:
            return False
    
    elif text.endswith("-"):
        if len(text.split("-"))-1 < 2 and len(text.split("E"))-1 == 1 and text.endswith("E-"):
            return True
        else:
            return False
    
    else:
        try:
            float(text)
            return True
        except:
            return False
    
        
def realpP(text):
    if text == "":
        return True
    
    elif text.startswith("E"):
        return False
    
    elif text.endswith("E"):
        if len(text.split("E"))-1 < 2:
            return True
        else:
            return False
    
    elif text.endswith("+"):
        if len(text.split("+"))-1 < 2 and len(text.split("E"))-1 == 1 and text.endswith("E+"):
            return True
        else:
            return False
    
    else:
        try:
            float(text)
            return True
        except:
            return False

    
def perc(text):
    if text == "": return True
    try:
        text = float(text)
        if text < 100:
            return True
        else:
            return False
    except:
        return False

ventana = tk.Tk()

ventana.geometry("650x410")
ventana.title("Calculadora de microbios")

ventana.iconbitmap(True, "parasite.ico")

# Generando el control de las pestañas

tabControl = ttk.Notebook(ventana)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)

tabControl.add(tab1, text = "UFC/mL o g")
tabControl.add(tab2, text = "NMP Coliformes")
tabControl.add(tab3, text = "NMP Diluciones")
tabControl.add(tab4, text = "Base seca")
tabControl.add(tab5, text = "Acerca de")
tabControl.pack(expand=1, fill="both")

# Cada widget que se añade a una pestaña debe contener la pestaña tabX
# tab1 = UFC
# tab2 = NMP Col
# tab3 = NMP Dil

## A partir de aquí inicia UFC/mL

col1 = ttk.Label(tab1,
                 text="Introduzca el número de colonias presentes: ")
col1.grid(column = 0,
            row = 0,
            padx = 15,
            pady = 5)

Ucol1 = ttk.Entry(tab1, 
                  validate="key", 
                  validatecommand=(ventana.register(entero), "%S"))

Ucol1.grid(column = 1,
            row = 0,
            padx = 15,
            pady = 5)



alic1 = ttk.Label(tab1,
                  text="Introduzca los mL transferidos a la caja Petri: ")
alic1.grid(column = 0,
            row = 1,
            padx = 15,
            pady = 5)

Ualic1 = ttk.Entry(tab1,
                   validate="key", 
                  validatecommand=(ventana.register(realp), "%P"))

Ualic1.grid(column = 1,
            row = 1,
            padx = 15,
            pady = 5)


dil1 = ttk.Label(tab1,
                 text="Introduzca la dilución: \n (pej. si es 10^-2 = introducir 1E-2)")

dil1.grid(column = 0,
            row = 2,
            padx = 15,
            pady = 5)


Udil1 = ttk.Entry(tab1,
                  validate="key", 
                  validatecommand=(ventana.register(realp), "%P"))

Udil1.grid(column = 1,
            row = 2,
            padx = 15,
            pady = 5)

def get_eq():
    col = Ucol1.get()
    alic = Ualic1.get()
    dil = Udil1.get()
    try:
        col = int(col)
    except:
        col = 0
    try:
        alic = float(alic)
    except:
        alic = 0.1
    try:
        dil = float(dil)
    except:
        dil = 1e-2
    ufc = Calculos.ufc_u(col, alic, dil)
    ufc = "{:e}".format(ufc)
    ufc = ufc.split("e")
    dil = "{:e}".format(dil)
    dil = dil.split("e")
    tmptext = r"$" + str(int(col)) + r" \ UFC \times \frac{1}{" + str(float(alic)) + r" \ mL} \times \frac{1}{" + str(float(dil[0])) + r" \times 10 ^{" + str(int(dil[1])) +"}} = " + str(float(ufc[0])) + r" \times 10 ^{" + str(int(ufc[1])) + r"} \ UFC/mL$"
    return tmptext

def get_eq2():
    a = int(ascr2.get())
    b = int(bscr2.get())
    c = int(cscr2.get())
    cal = Calculos.cal_col(a,b,c)
    eq = r"$ \frac{ (" + str(a) + r" + " + str(b) + r" + " + str(c) + r" ) \times 100 }{ \sqrt{ 10 \times (3 - " + str(a) + r") + 1 \times (3 - " + str(b) + r") + 0.1 \times (3 - " + str(c) + r" )}} = " + str(round(float(cal), 4)) + r" \ NMP/100 \ mL$"
    return eq

def get_eq3():
    a = int(ascr3.get())
    b = int(bscr3.get())
    c = int(cscr3.get())
    dil = float(dscr4.get())
    no_dil = float(Calculos.nmp_dil(a,b,c,1e-2))
    nmp = float(Calculos.nmp_dil(a,b,c,dil))
    
    dil = "{:e}".format(dil)
    dil = dil.split("e")
    
    nmp = "{:e}".format(nmp)
    nmp = nmp.split("e+")
    
    eq = r"$\frac{" + str(no_dil) + r"\ NMP/mL}{100} \times " + r"\frac{1}{"+ str(round(float(dil[0]),4)) + r" \times 10^{ " + str(dil[1]) + r" }} = " + str(round(float(nmp[0]),4)) + r" \times 10 ^{ " + str(nmp[1])  + r"}\ NMP/mL$"
    return eq

def get_eq3less():
    a = int(ascr3.get())
    b = int(bscr3.get())
    c = int(cscr3.get())
    dil = float(dscr4.get())
    no_dil = float(Calculos.nmp_dil(a,b,c,1e-2))
    nmp = float(Calculos.nmp_dil(a,b,c,dil))
    
    dil = "{:e}".format(dil)
    dil = dil.split("e")
    
    nmp = "{:e}".format(nmp)
    nmp = nmp.split("e+")
    
    eq = r"$\frac{ <" + str(no_dil) + r"\ NMP/mL}{100} \times " + r"\frac{1}{"+ str(round(float(dil[0]),4)) + r" \times 10^{ " + str(dil[1]) + r" }} = < " + str(round(float(nmp[0]),4)) + r" \times 10 ^{ " + str(nmp[1])  + r"}\ NMP/mL$"
    return eq

def get_eq3more():
    a = int(ascr3.get())
    b = int(bscr3.get())
    c = int(cscr3.get())
    dil = float(dscr4.get())
    no_dil = float(Calculos.nmp_dil(a,b,c,1e-2))
    nmp = float(Calculos.nmp_dil(a,b,c,dil))
    
    dil = "{:e}".format(dil)
    dil = dil.split("e")
    
    nmp = "{:e}".format(nmp)
    nmp = nmp.split("e+")
    
    eq = r"$\frac{ >" + str(no_dil) + r"\ NMP/mL}{100} \times " + r"\frac{1}{"+ str(round(float(dil[0]),4)) + r" \times 10^{ " + str(dil[1]) + r" }} = > " + str(round(float(nmp[0]),4)) + r" \times 10 ^{ " + str(nmp[1])  + r"}\ NMP/mL$"
    return eq

def get_eq4():

    mic = float(bse4.get())
    hum = round(float(hum4.get()),4)    
    bs = float(Calculos.bs(mic, hum))
    
    bs = "{:e}".format(bs)
    bs = bs.split("e+")
    
    mic = "{:e}".format(mic)
    mic = mic.split("e+")
    
       
    eq = r"$\frac{ " + str(round(float(mic[0]),4)) + r" \times 10^{" + str(mic[1]) + r" } }{ 1 - \frac{ " + str(hum) + r" \% }{100 \%}} = " + str(round(float(bs[0]),4)) + r" \times 10^{" + str((bs[1])) + r"}$"
    return eq

def get_ufc():
    col = Ucol1.get()
    alic = Ualic1.get()
    dil = Udil1.get()
    
    try:
        col = int(col)
    except:
        col = 0
    try:
        alic = float(alic)
    except:
        alic = 0.1
    try:
        dil = float(dil)
    except:
        dil = 1e-2
        
    ufc = Calculos.ufc_u(col, alic, dil)
    nufc = "{:e}".format(ufc)
    rufc = nufc.split("e")
    boxUFC["text"] = (str(ufc) + " UFC/mL \n" + str(float(rufc[0])) + " x 10^" + str(int(rufc[1])) + " UFC/mL")
    
    figure1 = plt.Figure(figsize=(3.8,1), dpi=100)
    #figure1.text(0, 0.5, '$8 \\ UFC \\times \\frac{1}{8.0 \\ mL} \\times \\frac{1}{1.0 \\times 10 ^{2}} = 1.0 \\times 10 ^{+02} \\ UFC/mL$')
    figure1.text(0, 0.5, get_eq())
    bar1 = FigureCanvasTkAgg(figure1, tab1)
    bar1.get_tk_widget().grid(column = 0,
                            row = 5,
                            padx = 15,
                            pady = 5)
    
    if col < 25 or col > 300:
        alert["text"] = "ADVERTENCIA:\nEl número de colonias \nno está entre\n25-250 ni 30-300."
    else:
        alert["text"] = ""
        
        
def get_bs():
    mic = float(bse4.get())
    hum = float(hum4.get())
    bs = round(Calculos.bs(mic, hum), 4)
    bs = "{:e}".format(bs)
    bs = bs.split("e+")
    
    
    boxBS["text"] = str(round(Calculos.bs(float(bse4.get()),float(hum4.get())),4)) + " UFC/mL o NMP/mL\n" + str(bs[0]) + " x 10^"+ str(round(int(bs[1]),4)) +" UFC/mL o NMP/mL"
    
    figure1 = plt.Figure(figsize=(3.8,1), dpi=100)
    figure1.text(0.2, 0.5, get_eq4(), fontsize=14)
    bar1 = FigureCanvasTkAgg(figure1, tab4)
    bar1.get_tk_widget().grid(column = 0,
                            row = 3,
                            padx = 15,
                            pady = 5)
    
    
        
        
ufc_exe = ttk.Button(tab1,
                     text = "Calcular",
                     command=get_ufc)

ufc_exe.grid(column = 0,
            row = 3,
            padx = 15,
            pady = 5)
    
boxUFC = ttk.Label(tab1)
boxUFC.grid(column = 0,
            row = 6,
            padx = 15,
            pady = 5)


alert = ttk.Label(tab1)
alert.grid(column = 1,
            row = 5,
            padx = 15,
            pady = 5)

op = ttk.Label(tab1,
               text="Operación:")
op.grid(column = 0,
        row = 4,
        padx = 15,
        pady = 5)

fig = plt.Figure(figsize=(3.8,1), dpi=100)
estante = FigureCanvasTkAgg(fig, tab1)
estante.get_tk_widget().grid(column = 0,
                            row = 5,
                            padx = 15,
                            pady = 5)



## Aquí termina UFC/mL

## A partir de aquí inicia NMP Coliformes



t1 = ttk.Label(tab2, text = "Tubos positivos con 10 mL:")
t1.grid(column = 0,
        row = 0,
        padx = 5,
        pady = 5)

ascr2 = tk.Scale(tab2, from_ = 0, to = 3, orient="horizontal")
ascr2.grid(column = 1,
          row = 0,
          padx = 15,
          pady = 5)
#ascr2.set("0")


t2 = ttk.Label(tab2, text = "Tubos positivos con 1 mL:")
t2.grid(column = 0,
        row = 1,
        padx = 15,
        pady = 5)

bscr2 = tk.Scale(tab2, from_ = 0, to = 3, orient="horizontal", variable="tk.IntVar")
bscr2.grid(column = 1,
          row = 1,
          padx = 15,
          pady = 5)


t3 = ttk.Label(tab2, text = "Tubos positivos con 0.1 mL:")
t3.grid(column = 0,
        row = 2,
        padx = 15,
        pady = 5)

cscr2 = tk.Scale(tab2, from_ = 0, to = 3, orient="horizontal")
cscr2.grid(column = 1,
          row = 2,
          padx = 15,
          pady = 5)

def get_col():
    a = int(ascr2.get())
    b = int(bscr2.get())
    c = int(cscr2.get())
    try:
        col = Calculos.nmp_col(a, b, c)
        boxCol["text"] = col + " NMP/100 mL de muestra"
        alert2["text"] = ""
        figure1 = plt.Figure(figsize=(3.8,1), dpi=100)
        bar1 = FigureCanvasTkAgg(figure1, tab2)
        bar1.get_tk_widget().grid(column = 0,
                                  row = 6,
                                  padx = 15,
                                  pady = 5)
        
    except:
        col = Calculos.cal_col(a,b,c)
        boxCol["text"] = col + " NMP/100 mL de muestra --- Ha sido calculado"
        alert2["text"] = "ADVERTENCIA:\nLos números\n calculados\n teóricamente\n deberían\n ser rechazados."
        
        figure1 = plt.Figure(figsize=(3.8,1), dpi=100)
        #figure1.text(0, 0.5, '$A$')
        figure1.text(0, 0.5, get_eq2())
        bar1 = FigureCanvasTkAgg(figure1, tab2)
        bar1.get_tk_widget().grid(column = 0,
                                  row = 6,
                                  padx = 15,
                                  pady = 5)
        
        
def get_nmp():
    a = int(ascr3.get())
    b = int(bscr3.get())
    c = int(cscr3.get())
    dil = float(dscr4.get())
    figure1 = plt.Figure(figsize=(3.8,1), dpi=100)
    
    if dil == 1e-2:
        nmp = float(Calculos.nmp_dil(a,b,c,1e-2))
        nmpe = "{:e}".format(nmp)
        nmpe = nmpe.split("e+")
        
        #figure1.text(0, 0.5, get_eq3less())
        bar1 = FigureCanvasTkAgg(figure1, tab3)
        bar1.get_tk_widget().grid(column = 0,
                                row = 5,
                                padx = 15,
                                pady = 5)
        
        if a == 0 and b == 0 and c == 0:
            nmpBox["text"] = "< " + str(nmp) + " NMP/mL\n< " + str(float(nmpe[0])) + " x 10^ " + str(nmpe[1]) + " NMP/mL"
        
        elif a == 3 and b == 3 and c == 3:
            nmpBox["text"] = "> " + str(nmp) + " NMP/mL\n> " + str(float(nmpe[0])) + " x 10^ " + str(nmpe[1]) + " NMP/mL"
        
        else:
            nmpBox["text"] = str(nmp) + " NMP/mL\n" + str(float(nmpe[0])) + " x 10^ " + str(nmpe[1]) + " NMP/mL"
        
    else:
        nmp = float(Calculos.nmp_dil(a,b,c,dil))
        nmpe = "{:e}".format(nmp)
        nmpe = nmpe.split("e+")
        
        #nmpBox["text"] = str(nmp) + " NMP/mL\n" + str(float(nmpe[0])) + " x 10^ " + str(nmpe[1]) + " NMP/mL"
        if a == 0 and b == 0 and c == 0:
            nmpBox["text"] = "< " + str(nmp) + " NMP/mL\n< " + str(float(nmpe[0])) + " x 10^ " + str(nmpe[1]) + " NMP/mL"
            figure1.text(0, 0.5, get_eq3less())
            bar1 = FigureCanvasTkAgg(figure1, tab3)
            bar1.get_tk_widget().grid(column = 0,
                                    row = 5,
                                    padx = 15,
                                    pady = 5)
        
        elif a == 3 and b == 3 and c == 3:
            nmpBox["text"] = "> " + str(nmp) + " NMP/mL\n> " + str(float(nmpe[0])) + " x 10^ " + str(nmpe[1]) + " NMP/mL"
            figure1.text(0, 0.5, get_eq3more())
            bar1 = FigureCanvasTkAgg(figure1, tab3)
            bar1.get_tk_widget().grid(column = 0,
                                    row = 5,
                                    padx = 15,
                                    pady = 5)
        
        else:
            nmpBox["text"] = str(nmp) + " NMP/mL\n" + str(float(nmpe[0])) + " x 10^ " + str(nmpe[1]) + " NMP/mL"
            
        
        #figure1.text(0, 0.5, '$A$')
            figure1.text(0, 0.5, get_eq3())
            bar1 = FigureCanvasTkAgg(figure1, tab3)
            bar1.get_tk_widget().grid(column = 0,
                                    row = 5,
                                    padx = 15,
                                    pady = 5)
            
        
        
        
    
    
    
    

boxCol = ttk.Label(tab2, text = "")
boxCol.grid(column = 0,
            row = 5,
            padx = 15,
            pady = 5)

obCol = ttk.Button(tab2, text="Obtener",
                   command=get_col)

obCol.grid(column = 0,
           row = 4,
           padx = 15,
           pady = 5)

#fig = plt.Figure(figsize=(3.8,1), dpi=100)
estante = FigureCanvasTkAgg(fig, tab2)
estante.get_tk_widget().grid(column = 0,
                            row = 6,
                            padx = 15,
                            pady = 5)

alert2 = ttk.Label(tab2,
                   text="")
alert2.grid(column = 1,
            row = 6,
            padx = 15,
            pady = 5)

## Aquí acaba NMP Coliformes

## Aquí inicia NMP Diluciones tab3

s1 = ttk.Label(tab3,
               text = "Tubos positivos con la dilución menor:\n(10^-1 por defecto)")
s1.grid(column = 0,
        row = 0,
        padx = 5,
        pady = 5)

s2 = ttk.Label(tab3,
               text = "Tubos positivos con la dilución intrmedia:\n(10^-2 por defecto)")

s2.grid(column = 0,
        row = 1,
        padx = 5,
        pady = 5)

s3 = ttk.Label(tab3,
               text = "Tubos positivos con la dilución mayor:\n(10^-3 por defecto)")

s3.grid(column = 0,
        row = 2,
        padx = 5,
        pady = 5)

ascr3 = tk.Scale(tab3, from_ = 0, to = 3, orient="horizontal")
ascr3.grid(column = 1,
          row = 0,
          padx = 15,
          pady = 5)

bscr3 = tk.Scale(tab3, from_ = 0, to = 3, orient="horizontal", variable="tk.IntVar")
bscr3.grid(column = 1,
          row = 1,
          padx = 15,
          pady = 5)

cscr3 = tk.Scale(tab3, from_ = 0, to = 3, orient="horizontal")
cscr3.grid(column = 1,
          row = 2,
          padx = 15,
          pady = 5)



s4 = ttk.Label(tab3, 
              text="Cambiar la dilución intermedia:\n(pej. si es 10^-4 = introducir 1E-4)")

s4.grid(column = 0,
        row = 3,
        padx = 15,
        pady = 5)

dscr4 = ttk.Entry(tab3,
                  validate="key", 
                  validatecommand=(ventana.register(realp), "%P"))
dscr4.grid(column = 1,
          row = 3,
          padx = 15,
          pady = 5)

dscr4.insert(0,"1E-2")


obNmp = ttk.Button(tab3,
                   text="Obtener",
                   command=get_nmp)

obNmp.grid(column = 0,
          row = 4,
          padx = 15,
          pady = 5)

nmpBox = ttk.Label(tab3,
                   text="")

nmpBox.grid(column = 1,
            row = 5,
            padx = 15,
            pady = 5)


#fig = plt.Figure(figsize=(3.8,1), dpi=100)
estante = FigureCanvasTkAgg(fig, tab3)
estante.get_tk_widget().grid(column = 0,
                            row = 5,
                            padx = 15,
                            pady = 5)

## Aquí termina NMP

## Aquí empieza Base seca

absl4 = ttk.Label(tab4,
                text = "Introduce las UFC/mL o NMP/mL:\n")
absl4.grid(column = 0,
         row = 0,
         padx = 15,
         pady = 5)

bbsl4 = ttk.Label(tab4,
                  text = "Introduce el porcentaje de humedad:\n(pej. 40% = introduce 40)")
bbsl4.grid(column = 0,
           row = 1,
           padx = 15,
           pady = 5)


bse4 = ttk.Entry(tab4,
                 validate = "key",
                 validatecommand=(ventana.register(realpP), "%P"))
                 
bse4.grid(column = 1,
           row = 0,
           padx = 15,
           pady = 5)

hum4 = ttk.Entry(tab4,
                 validate = "key",
                 validatecommand=(ventana.register(perc), "%P"))

hum4.grid(column = 1,
           row = 1,
           padx = 15,
           pady = 5)

obBs = ttk.Button(tab4,
                   text = "Calcular",
                   command = get_bs)

obBs.grid(column = 0,
           row = 2,
           padx = 15,
           pady = 5)

boxBS = ttk.Label(tab4,
                  text = "")

boxBS.grid(column = 0,
           row = 4,
           padx = 15,
           pady = 5)


fig = plt.Figure(figsize=(3.8,1), dpi=100)
estante = FigureCanvasTkAgg(fig, tab4)
estante.get_tk_widget().grid(column = 0,
                            row = 3,
                            padx = 15,
                            pady = 5)

## Aquí termina Base seca

## Empieza acerca de

def github():
    webbrowser.open(r"https://github.com/Changeryto")
    
def linkedin():
    webbrowser.open(r"https://mx.linkedin.com/in/rub%C3%A9n-t%C3%A9llez-gerardo-411160228?trk=people-guest_people_search-card")
    
def telegram():
    webbrowser.open(r"https://t.me/Senado_y_Pueblo_de_Roma")
    
def workana():
    webbrowser.open(r"https://www.workana.com/freelancer/de131a3750c133dfcda37ae808b2fedc")

def ptico():
    webbrowser.open("https://www.pinterest.com/pin/create/bookmarklet/?media=https://cdn-icons-png.flaticon.com/512/1186/1186545.png&description=Download now this vector icon in SVG, PSD, PNG, EPS format or as webfonts. Flaticon, the largest database of free icons.&url=https://www.flaticon.com/free-icon/parasite_1186545&is_video={video}")

ad5 = ttk.Label(tab5,
                text="\n05/01/2022 Calculadora de microbios. v1.0.0")

ad5.pack()

bad5 = ttk.Label(tab5,
                 text="Programado en Python por Rubén Téllez Gerardo\nTécnico L.Q. y estudiante de Q.B.P. en el IPN")

bad5.pack()

bad5 = ttk.Label(tab5,
                 text="Si el programa te fué de ayuda agradecería enormemente que lo compartieras.")

bad5.pack()

cad5 = ttk.Label(tab5,
                 text="\nPuedes contactarme en:\n")
cad5.pack()

tl = ttk.Button(tab5,
                text="Telegram",
                command=telegram)
tl.pack()

li = ttk.Button(tab5,
                text="LinkedIn",
                command=linkedin)

li.pack()

gh = ttk.Button(tab5,
                text = "GitHub",
                command=github)


gh.pack()

wk = ttk.Button(tab5,
                text="Workana",
                command=workana)
wk.pack()

dad5 = ttk.Label(tab5,
                 text="\n¡Espero haberte ayudado con esos cálculos!")

dad5.pack()

ead5 = ttk.Label(tab5,
                 text="Siempre disponible para desarrollo y afines a ciencias químico-biológicas.\n\n")

ead5.pack()


pt = ttk.Button(tab5,
                   text="Referencia del icono",
                   command=ptico)

pt.pack()

ventana.mainloop()


if __name__ == '__main__':
    pass