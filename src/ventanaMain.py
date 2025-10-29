import customtkinter as ctk
import tkinter as tk
from controlador import descargarArchivo
from directory import abrirDir
import tkinter.messagebox as messagebox
import os
from version import VERSION

TIPO_VIDEO = "video"
TIPO_AUDIO = "audio"

class VentanaDownloader:
    def __init__(self):
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
        
        version_label = ctk.CTkLabel(master=main_frame, text=f"Versión: {VERSION}", fg_color="transparent")
        version_label.pack(side="bottom", pady=5)

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
        frame_opciones = self._crear_frame(parent, 250, 40)
        frame_opciones.pack(pady=5)

        radio_audio = ctk.CTkRadioButton(master=frame_opciones, text="Audio", variable=self.media_var, value=TIPO_AUDIO)
        radio_audio.pack(side=ctk.LEFT, padx=5, pady=5)

        radio_video = ctk.CTkRadioButton(master=frame_opciones, text="Video", variable=self.media_var, value=TIPO_VIDEO)
        radio_video.pack(side=ctk.RIGHT, padx=5, pady=5)
    
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
        
        self.btn_descarga = ctk.CTkButton(master=frame_btn, text="Descargar", command=self._iniciar_descarga)
        self.btn_descarga.grid(row=0, column=0, padx=10)
        
        btn_carpeta = ctk.CTkButton(master=frame_btn, text="Carpeta de descarga",
                                    command=lambda: abrirDir(self.obtener_seleccion()))
        btn_carpeta.grid(row=0, column=1, padx=10)
    
    # --- Barra de progreso ---
    def _add_progress_bar(self, parent):
        self.progress_bar = ctk.CTkProgressBar(master=parent, width=430, height=20)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
    
    
    # --- Label de mensajes ---
    def _add_message_label(self, parent):
        
        self.label_msg = ctk.CTkLabel(master=parent, text="", fg_color="transparent", wraplength=400, justify="center")
        self.label_msg.pack(pady=5)
    
    def update_message(self, text):
        if "Descarga completa" in text:
            color = "#1F6AA5"
        elif "Error" in text:
            color = "#FF0000"
        elif "ya existe" in text:
            color = "#FFA500"
        else:
            color = "#ffffff"

        fuente = ("Arial",14, "bold")
        self.label_msg.configure(text=text, text_color=color, font=fuente)
    
    # --- Función de descarga ---
    def _iniciar_descarga(self):
        url = self._url_entry.get().strip()
        if not url:
            self.update_message("Error: La URL ingresada está vacía")
            return
        self.btn_descarga.configure(state="disabled")
        def actualizar_mensaje_y_reactivar(texto):
            self.update_message(texto)
            if "Descarga completa" in texto or "Error" in texto or "ya existe" in texto:
                self.btn_descarga.configure(state="normal")
        descargarArchivo(self.obtener_seleccion(),
                         url,
                         progress_bar=self.progress_bar,
                         update_message=actualizar_mensaje_y_reactivar)
        self._url_entry.delete(0, tk.END)
    
    # --- Iniciar GUI ---
    def run(self):
        self.root.mainloop()
    

if __name__ == "__main__":
    app = VentanaDownloader()
    app.run()