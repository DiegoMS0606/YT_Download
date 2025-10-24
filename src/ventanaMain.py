import customtkinter as ctk
import tkinter as tk
from controlador import descargarArchivo
from directory import abrirDir
import tkinter.messagebox as messagebox
import os


TIPO_VIDEO = "video"
TIPO_AUDIO = "audio"

class VentanaDownloader:
    def __init__(self, root):
        self.root = ctk.CTk()
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.root.title("Downloader")
        self.root.geometry("480x480")
        self.root.minsize(480,480)
        self.root.maxsize(480,480)
        
        self.media_var = tk.StringVar(value=TIPO_VIDEO)
        self._crear_widgets()
    
    def _crear_widgets(self):
        main_frame = self._crear_frame(self.root, 450, 450)
        main_frame.pack(pady=15)
        
        self._solicitar_link(main_frame)
        self._opcion_box(main_frame)
        self._box_descarga(main_frame)
        self._add_progress_bar(main_frame)
        self._add_message_label(main_frame)

    def _crear_frame(self, root, width, height):
        frame = ctk.CTkFrame(master=root, width=width, height=height,fg_color="transparent")
        frame.pack_propagate(False)
        return frame
    
    def _label(self, root, txt):
        label = ctk.CTkLabel(master=root, text=txt, fg_color="transparent")
        label.pack()
        return label
    
    def _solicitar_link(self, main):
        frameSL = self._crear_frame(main,450,70)
        frameSL.pack(pady=5)
        self._label(frameSL, 'Ingresa el link:')
        self._url_entry = ctk.CTkEntry(master=frameSL, width=430, height=40)
        self._url_entry.pack(pady=5)
    
    def _opcion_box(self, parent):
        frame_opciones = self._crear_frame(parent, 430, 40)
        frame_opciones.pack_propagate()
        frame_opciones.grid_columnconfigure(0, weight=1)
        frame_opciones.grid_columnconfigure(1, weight=1)
        
        self._crear_radio(frame_opciones, "Audio", TIPO_AUDIO, 0)
        self._crear_radio(frame_opciones, "Video", TIPO_VIDEO, 1)
    
    def _crear_radio(self, parent, texto, valor, col):
        frame = self._crear_frame(parent, 80, 35)
        frame.grid(row=0, column=col, padx=10)
        radio = ctk.CTkRadioButton(master=frame, text=texto, variable=self.media_var, value=valor)
        radio.pack(padx=5, pady=5, side=ctk.LEFT)
    
    def obtener_seleccion(self):
        return self.media_var.get()
    
    def _box_descarga(self, parent):
        frame_btn = self._crear_frame(parent, 430, 60)
        frame_btn.pack(pady=10)
        frame_btn.grid_columnconfigure(0, weight=1)
        frame_btn.grid_columnconfigure(1, weight=1)
        
        btn_descarga = ctk.CTkButton(master=frame_btn, text="Descargar", command=self._iniciar_descarga)
        btn_descarga.grid(row=0, column=0, padx=10)
        
        btn_carpeta = ctk.CTkButton(master=frame_btn, text="Carpeta de descarga",
                                    command=lambda: abrirDir(self.obtener_seleccion()))
        btn_carpeta.grid(row=0, column=1, padx=10)
    
    # --- Barra de progreso ---
    def _add_progress_bar(self, parent):
        self.progress_bar = ctk.CTkProgressBar(master=parent, width=430, height=20)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
    
    def _actualizar_color_barra(self):
        if self.obtener_seleccion() == TIPO_VIDEO:
            self.progress_bar.configure(fg_color="red")
        else:
            self.progress_bar.configure(fg_color="blue")  # audio: azul
    
    # --- Label de mensajes ---
    def _add_message_label(self, parent):
        self.label_msg = ctk.CTkLabel(master=parent, text="", fg_color="transparent")
        self.label_msg.pack(pady=5)
    
    def update_message(self, text):
        self.label_msg.configure(text=text)
    
    # --- Función de descarga ---
    def _iniciar_descarga(self):
        url = self._url_entry.get().strip()
        if not url:
            self.update_message("Error: La URL ingresada está vacía")
            return
        
        self._actualizar_color_barra()
        descargarArchivo(self.obtener_seleccion(),
                         url,
                         progress_bar=self.progress_bar,
                         update_message=self.update_message)
        self._url_entry.delete(0, tk.END)
    
    # --- Iniciar GUI ---
    def run(self):
        self.root.mainloop()
    

if __name__ == "__main__":
    app = VentanaDownloader()
    app.run()