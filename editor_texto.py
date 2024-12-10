import tkinter as tk
from tkinter import Scrollbar,RIGHT,Y,filedialog,messagebox,font

# Le damos nombre,tamaño y color a la ventana
raiz = tk.Tk()
raiz.title("Editor de texto")
raiz.geometry("800x600")
raiz.config(bg="#f0fff0")

# Creamos la barra de desplazamiento y le decimos en que lugar la queremos
scroll = Scrollbar(raiz)
scroll.pack(side=RIGHT, fill=Y)

# Creamos un area para poder escribir y la sincronizamos con la barra vertical
texto = tk.Text(raiz,wrap="word",yscrollcommand=scroll.set,font=("arial",18))
texto.place(relx=0.5,rely=0.54,anchor="center",relwidth=0.9,relheight=0.90)
scroll.config(command=texto.yview)

# Creamos una cadena vacia para a la hora de cerrar el programa poder comparar si hay cambios en el texto
contenido_guardado = ""

# Creamos una funcion para poder seleccionar todo el texto con control-a
def seleccionar_texto(accion):
    texto.tag_remove("sel","1.0","end")
    texto.tag_configure("sel", background="lightblue", foreground="black")
    
    # Al seleccionar todo solo se nos marca el texto y no todo a lo horizontal donde no hay texto
    num_lineas = int(texto.index("end-1c").split(".")[0])  
    for i in range(1, num_lineas + 1):
        inicio_linea = f"{i}.0"  
        fin_linea = texto.index(f"{i}.end")  
        if texto.get(inicio_linea, fin_linea).strip():  
           texto.tag_add("sel", inicio_linea, fin_linea)  
    return "break"
# Funcion para poder abrir documentos y cargarlos en el programa
def abrir_documento():
    global contenido_guardado
    ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto","*.txt"),("Todos los archivos","*.*")])
    if ruta:
        try:
            with open(ruta,"r") as documento:
                contenido = documento.read()
                texto.delete("1.0", tk.END)
                texto.insert(tk.END, contenido)
        except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {str(e)}")

# Le damos al usuario la opcion de poder guardar el documento
def guardar_documento():
    global contenido_guardado
    ruta = filedialog.asksaveasfilename(filetypes=[("Archivos de texto","*.txt"),("Todos los archivos","*.*")])
    contenido = texto.get("1.0",tk.END)
    if ruta:
        try:
            with open(ruta,"w") as documento:
                documento.write(contenido)
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo guardar el archivo: {str(e)}")

texto.tag_configure("negrita", font=("arial", 18, "bold"))
texto.tag_configure("cursiva", font=("arial", 18, "italic"))
texto.tag_configure("subrayado", font=("arial", 18, "underline"))

# Funcion para poder convertir el texto a negrita
def aplicar_negrita():
    try:
        # Intentamos obtener el rango del texto seleccionado
        inicio = texto.index(tk.SEL_FIRST)
        fin = texto.index(tk.SEL_LAST)

        if "negrita" in texto.tag_names(inicio):
            texto.tag_remove("negrita", inicio, fin)
        else:
            texto.tag_add("negrita", inicio, fin)
     
    # Si el usuario no ha seleccionado una parte concreta del texto, aplica negrita a todo el texto 
    except tk.TclError:
        if "negrita" in texto.tag_names("1.0"):
            texto.tag_remove("negrita", "1.0", tk.END)
        else:
            texto.tag_add("negrita", "1.0", tk.END)

# Funcion para poder convertir el texto a cursiva
def aplicar_cursiva():
     try:
        # Intentamos obtener el rango del texto seleccionado
        inicio = texto.index(tk.SEL_FIRST)
        fin = texto.index(tk.SEL_LAST)

        if "cursiva" in texto.tag_names(inicio):
           texto.tag_remove("cursiva", inicio,fin)
        else:
           texto.tag_add("cursiva", inicio,fin)
  
     # Si el usuario no ha seleccionado una parte concreta del texto, aplica la letra cursiva a todo el texto 
     except tk.TclError:
         if "cursiva" in texto.tag_names("1.0"):
           texto.tag_remove("cursiva", "1.0", tk.END)
         else:
           texto.tag_add("cursiva", "1.0", tk.END)
               
# Funcion para poder convertir el texto subrayado
def aplicar_subrayado():
    try:
        # Intentamos obtener el rango del texto seleccionado
        inicio = texto.index(tk.SEL_FIRST)
        fin = texto.index(tk.SEL_LAST)

        if "subrayado" in texto.tag_names(inicio):
           texto.tag_remove("subrayado", inicio,fin)
        else:
           texto.tag_add("subrayado", inicio,fin)

    # Si el usuario no ha seleccionado una parte concreta del texto, aplica el subrayado a todo el texto
    except tk.TclError:
        if "subrayado" in texto.tag_names("1.0"):
           texto.tag_remove("subrayado", "1.0",tk.END)
        else:
           texto.tag_add("subrayado", "1.0",tk.END)

# Si le damos por error a la X, primero le preguntamos al usuario si está seguro, por si ha sido un error y no ha guardado 
def cerrar_ventana():
    contenido_actual = texto.get("1.0",tk.END).strip()
    if contenido_actual != contenido_guardado:
        respuesta = messagebox.askyesnocancel("Salir","Tienes cambios sin guardar. ¿Deseas guardar antes de salir?")
        if respuesta is None:
            return
        elif respuesta:
            guardar_documento()
    raiz.destroy()    


boton = tk.Menu(raiz)
raiz.config(menu=boton)
archivo_menu = tk.Menu(boton,tearoff=0)
boton.add_cascade(label="Archivo",menu=archivo_menu)
archivo_menu.add_command(label="Abrir",command=abrir_documento)
archivo_menu.add_command(label="Guardar",command=guardar_documento)
archivo_menu.add_separator()
archivo_menu.add_command(label="Salir",command=cerrar_ventana)


botonNegrita = tk.Button(raiz,text="Negrita",font=("utopia",12,"bold"),command=aplicar_negrita)
botonNegrita.place(relx=0.3,rely=0.045,relwidth=0.1,anchor="center")

botonCursiva = tk.Button(raiz,text="Cursiva",font=("utopia",12,"italic"),command=aplicar_cursiva)
botonCursiva.place(relx=0.5,rely=0.045,relwidth=0.1,anchor="center")

fuenteSubrayada = font.Font(family="Utopia",underline=True)

botonSubrayado = tk.Button(raiz,text="Subrayado",font=fuenteSubrayada,command=aplicar_subrayado)
botonSubrayado.place(relx=0.7,rely=0.045,relwidth=0.15,anchor="center")

texto.bind("<Control-a>",seleccionar_texto)
raiz.protocol("WM_DELETE_WINDOW", cerrar_ventana)

raiz.mainloop()
