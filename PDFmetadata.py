import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb
import PyPDF2
import os

def procesar_pdf():
    mydir = ("Documents")
    mydir = os.path.abspath(mydir) 
    
    file_path = filedialog.askopenfilename \
        (initialdir=mydir, title="Seleccionar archivo PDF", \
        filetypes=(("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")))
    if not file_path:
        raise FileNotFoundError      
    try:
        with open(file_path, "rb") as archivo:

            #Lector
            lector = PyPDF2.PdfReader(archivo)
            texto = input_txt.get()
            if texto == '':
                texto = 'texto'+'.txt'
            else:
                texto += ".txt"
              
            os.makedirs(mydir, exist_ok=True) # Directorio donde se guardaran los txt generados 
            path = os.path.join(mydir, texto)
        
            for n in range(len(lector.pages)):
                page = lector._get_page(n)
                info = page.extract_text()
                with open(path, "w") as txt:
                    try:
                        txt.write(info)
                    except Exception as e:
                        print(f'Hubo un error al guardar el texto en el archivo: {e}')


            metadata_label.config(text=f"Título: {lector.metadata.title}\n"
                                            f"Autor: {lector.metadata.author}\n"
                                            f"Asunto: {lector.metadata.subject}\n"
                                            f"Palabras clave: {lector.metadata.get('/Keywords', 'No se encontraron palabras clave')}\n"
                                            f"Fecha de creación: {lector.metadata.get('/CreationDate', 'No se encontró fecha de creación')}"
                                            "\nArchivo creado con  éxito.")
            
            
        
    except FileNotFoundError:
        mb.showerror("Error", f"El archivo no existe")
    except Exception as e:
        mb.showerror("Error", f"Error inesperado: {e}")


root = tk.Tk()
root.title("PDFMetadata")
root.geometry("320x200")
root.config(bg="silver")
file="static/pdf.ico"
icono = tk.PhotoImage(file)
root.iconbitmap(True, icono)

num_columnas = 3


input_label = tk.Label(root, text="Nombre del archivo de texto:")
input_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")
input_txt = tk.Entry(root)
input_txt.grid(row=0, column=2, padx=5, pady=5, sticky="w")

# Botón selección archivo PDF
select_button = tk.Button(root, text="Seleccionar PDF", command=procesar_pdf)
select_button.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

# mostrar metadatos del PDF
metadata_label = tk.Label(root, text="")
metadata_label.grid(row=3, column=0, columnspan=num_columnas, padx=5, pady=5)

root.mainloop()