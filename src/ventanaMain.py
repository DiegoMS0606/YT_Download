import customtkinter as ctk
import tkinter as tk
from controlador import descargarArchivo
from directory import abrirDir
import tkinter.messagebox as messagebox
import os

media = None

def ventana():
    main = ctk.CTk()
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    main.title("Downloader")

    main.geometry("480x480")
    main.minsize(480,480)
    main.maxsize(480,480)
    
    principal(main)
    

    main.mainloop()
    

    
def frame(root, width, height):
    frame = ctk.CTkFrame(master=root, width=width, height=height,fg_color="transparent")
    frame.pack()
    frame.pack_propagate(False)
    return frame

def label(root, txt):
    label = ctk.CTkLabel(master=root, text=txt, fg_color="transparent")
    label.pack()
    
def optionButton(main, text, var, valor):
    opcion = ctk.CTkRadioButton(main,text=text,variable=var,value=valor)
    return opcion

def button(main, text,command):
    boton = ctk.CTkButton(master=main,text=text,command=command)
    return boton
    
def principal(main):
    frameP = frame(main,450,450)
    frameP.pack(pady=15)
    global link
    solicitarLink(frameP)
    opcionBox(frameP)
    boxDescarga(frameP)
    addProgressBar(frameP)
    addMessageLabel(frameP)
    
def solicitarLink(main):
    
    frameSL = frame(main,450,70)
    frameSL.pack(pady=5)
    labelLink(frameSL)
    urlBox(frameSL)

    
def labelLink(main):
    frameL = frame(main,200,20)
    frameL.pack(pady=5)
    label(frameL,"Ingresa el link:")
    
def urlBox(main):
    global url
    url = ctk.CTkEntry(main, width=430,height=40)
    url.pack(pady=5)
    

def opcionBox(main):
    global media
    media = tk.StringVar(value="video")
    frameO = frame(main,430,40)
    frameO.pack_propagate()
    frameO.grid_columnconfigure(0,weight=1)
    frameO.grid_columnconfigure(1,weight=1)
    boxA(frameO)
    boxV(frameO)
    
def boxA(main):
    boxA = frame(main,80,35)
    boxA.grid(row=0,column=0,padx=10)
    opcionBoxA(boxA)
def boxV(main):
    boxV = frame(main,80,35)
    boxV.grid(row=0,column=1,padx=10)
    opcionBoxV(boxV)

def opcionBoxV(main):
    a = "video"
    video = optionButton(main,"Video",media,a)
    video.pack(padx=5,pady=5, side=ctk.LEFT)
    
def opcionBoxA(main):
    
    a = "audio"
    video = optionButton(main,"Audio",media,a)
    video.pack(padx=5,pady=5, side=ctk.LEFT)
    
def obtenerSeleccion():
    return media.get()
    
def boxDescarga(main):
    framD=frame(main, 430,60)
    framD.pack(pady=10)
    framD.grid_columnconfigure(0,weight=1)
    framD.grid_columnconfigure(1,weight=1)
    btnDescarga(framD)
    btnOpenDir(framD)
    
def btnDescarga(main):
    btn = button(main, "Descarga", limpiarYDescargar)  # Cambia aquí
    btn.grid(row=0, column=0, padx=10)
    
def limpiarYDescargar():
    url_value = url.get().strip()  # Obtén el valor de la URL y elimina espacios
    if url_value:  # Verifica si no está vacía
        actualizarColorBarra()
        descargarArchivo(obtenerSeleccion())  # Inicia la descarga
        url.delete(0, tk.END)  # Limpia la entrada de la URL
    else:
        print("Error: La URL ingresada está vacía.")
    
def btnOpenDir(main):
    btn = button(main, "Carepta de descarga",lambda:abrirDir(obtenerSeleccion()))
    btn.grid(row=0,column=1,padx=10)
    
def addProgressBar(main):
    global progress_bar
    progress_bar = ctk.CTkProgressBar(master=main, width=430, height=20)
    progress_bar.pack(pady=10)
    progress_bar.set(0)
    
def actualizarColorBarra():
    """Actualiza el color de la barra de progreso según el tipo de archivo seleccionado"""
    if obtenerSeleccion() == "video":
        progress_bar.configure(fg_color="red")
    
def addMessageLabel(main):
    global label_msg
    label_msg = ctk.CTkLabel(master=main, text="", fg_color="transparent")
    label_msg.pack(pady=5)

def updateMessage(text):
    label_msg.configure(text=text)