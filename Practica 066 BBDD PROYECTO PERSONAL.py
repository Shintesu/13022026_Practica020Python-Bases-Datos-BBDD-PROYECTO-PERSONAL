# PROYECTO PERSONAL
# CREACIÓN DE UNA BASE DE DATOS MANIPULABLE POR MEDIO DE UN PROGRAMA.

# librerías necesarias------------------------------------------------------------------
from tkinter import *
from tkinter import messagebox
import sqlite3 

# ventana-------------------------------------------------------------------------------
root = Tk ()
root.title("Base de Datos - PROYECTO PERSONAL")

MiFrame = Frame (root)
MiFrame.pack()


# conexión a la base de datos-----------------------------------------------------------
# definir función conectar
def infoConectar():
    MiConexion = sqlite3.connect("BaseDatosPruebaPersonal01")
    MiCursor = MiConexion.cursor()                                      # crear el cursor
    MiCursor.execute("""
    CREATE TABLE IF NOT EXISTS Usuarios (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOMBRE TEXT,
        PASSWORD TEXT,
        APELLIDO TEXT,
        DIRECCION TEXT
        )
    """)         # ejecuta el query

    MiConexion.commit()
    MiConexion.close()
    messagebox.showinfo("Función conectar", "Base de datos creada correctamente")

# botón crear--------------------
def Crear_Registro():
    MiConexion = sqlite3.connect("BaseDatosPruebaPersonal01")
    MiCursor = MiConexion.cursor()
    # obtener valores de los Entry
    CrearNombre = CuadroNombre.get()
    CrearPassword = CuadroPassword.get()
    CrearApellido = CuadroApellido.get()
    CrearDireccion = CuadroDireccion.get()
    # validar que no se encuentren vacíos
    if CrearNombre == "" or CrearPassword == "":
        messagebox.showwarning("Campos vacíos", "El nombre y la contraseña son campos obligatorios*")
        return
    # ejecutar el commando insert             /// hacer uso de las consultas paramétricas
    MiCursor.execute("INSERT INTO Usuarios (NOMBRE, PASSWORD, APELLIDO, DIRECCION) VALUES (?, ?, ?, ?)",
                 (CrearNombre, CrearPassword, CrearApellido, CrearDireccion))
    MiConexion.commit()
    MiConexion.close()
    Borrar_Campos()
    messagebox.showinfo("Registro creado", f"Usuario'{CrearNombre}' ha sido agregado correctamente")

# botón leer----------------------------------------------------------------------------------
def Leer_Registro():
    MiConexion = sqlite3.connect("BaseDatosPruebaPersonal01")
    MiCursor = MiConexion.cursor()
    # obtener valores del Entry Id usuario
    Id_Usuario = CuadroID.get()
    # validar que el ID no se encuentre vacío
    if Id_Usuario == "":
        messagebox.showwarning("ID vacía", "El ID de usuario es necesaria*")
        return 
    # ejecutar el commando insert
    try:    # buscar el registro con ese ID
        MiCursor.execute("SELECT * FROM Usuarios WHERE ID = ?", (Id_Usuario,))
        Usuario = MiCursor.fetchone()
        if Usuario: # limpiar los campos antes de mostrar los datos
            Borrar_Campos()
            CuadroID.insert(0, Usuario[0])    
            CuadroNombre.insert(0, Usuario[1]) 
            CuadroPassword.insert(0, Usuario[2]) 
            CuadroApellido.insert(0, Usuario[3]) 
            CuadroDireccion.insert(0, Usuario[4]) 
            messagebox.showinfo("Registro leído", f"Datos del usuario '{Usuario[1]}' cargados correctamente")  
        else:
            messagebox.showwarning("Sin resultados", f"No se encontraron los datos del usuario '{Usuario[1]}'")  
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al leer el registro del usuario '{Usuario[1]}'")
    finally:
        MiConexion.close()

# botón actualizar----------------------------------------------------------------------------
def Actualizar_Registro():
    MiConexion = sqlite3.connect("BaseDatosPruebaPersonal01")
    MiCursor = MiConexion.cursor()
    # obtener valores de los Entry
    Id_Usuario = CuadroID.get()
    ActualizarNombre = CuadroNombre.get()
    ActualizarPassword = CuadroPassword.get()
    ActualizarApellido = CuadroApellido.get()
    ActualizarDireccion = CuadroDireccion.get()
    # validar que no se encuentren vacíos
    if Id_Usuario == "":
        messagebox.showwarning("ID vacía", "El ID de usuario es necesario*")
        return 
    if ActualizarNombre == "" or ActualizarPassword == "":
        messagebox.showwarning("Campos vacíos", "El nombre y la contraseña son campos obligatorios*")
        return
    # ejecutar el commando insert
    try:
        MiCursor.execute("""
            UPDATE Usuarios SET NOMBRE= ?, PASSWORD= ?, APELLIDO= ?, DIRECCION= ? 
                         WHERE ID= ? """,
            (ActualizarNombre, ActualizarPassword, ActualizarApellido, ActualizarDireccion, Id_Usuario))
        if MiCursor.rowcount == 0:
            messagebox.showwarning("Sin resultados", "No se encontró ningún usuario con ese ID")
        else:
            messagebox.showinfo("Registro actualizado", f"Usuario'{ActualizarNombre}' ha sido actualizado correctamente")

    except Exception as e:
        messagebox.showinfo("Error", f"Ocurrió un error al actualizar: \n {e}")
    finally:
        MiConexion.commit()
        MiConexion.close()
        Borrar_Campos()
        

# botón eliminar-------------------------------------------------------------------------------
def Eliminar_Registro():
    MiConexion = sqlite3.connect("BaseDatosPruebaPersonal01")
    MiCursor = MiConexion.cursor()
    # obtener valores de los Entry
    Id_Usuario = CuadroID.get()
    # ejecutar el commando insert
    if Id_Usuario == "":
        messagebox.showwarning("ID vacía", "El ID de usuario es necesario*")
        return
    # confirmar eliminación de datos
    Respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar el usuario con ID '{Id_Usuario}'?")
    if not Respuesta:
        return              # si cancela no ocurre nada
    try:                    # ejecutar el comando delete
        MiCursor.execute("DELETE FROM Usuarios WHERE ID = ?", (Id_Usuario,))
        if MiCursor.rowcount == 0:
            messagebox.showwarning("Sin resultados", f"No se encontró ningún usuario con el ID '{Id_Usuario}'")
        else:
            messagebox.showinfo("Registro eliminado", f"Usuario con ID '{Id_Usuario}' eliminado correctamente")
            Borrar_Campos()
    except Exception as e:
           messagebox.showerror("Error", f"Ocurrió un error al eliminar el registro:\n{e}")
    finally:
        MiConexion.commit()
        MiCursor.close()


# ventanas emergentes-------------------------------------------------------------------
def infoBorrar():
    Borrar_Campos()                                     # llamamos a la función borrar campos
    messagebox.showinfo("Borrar", "Se ha borrado la información dentro de los campos")

def infoLicencia():
    messagebox.showinfo("Licencia", "La licencia del producto es válida")
def infoAcercaDe():
    messagebox.showinfo("Acerca de...", "Este programa es una proyecto de aprendizaje autodidacta para poner a prueba los conocimientos adquiridos")


def infoCrear():
    messagebox.showinfo("Crear", "Se ha creado un usuario dentro de la base de datos")
def infoLeer():
    messagebox.showinfo("Leer", "Se ha podido leer la información dentro de la base de datos")
def infoActualizar():
    messagebox.showinfo("Actualizar", "Se ha podido actualizar la información dentro de la base de datos")
def infoEliminar():
    messagebox.showinfo("Eliminar", "Se ha podido eliminar la información dentro de la base de datos")


# funcionalidad de borrar campos (resetear)---------------------------------------------
def Borrar_Campos():                                    # se crea la función de borrar campos
    CuadroID.delete(0, END)    
    CuadroNombre.delete(0, END)
    CuadroPassword.delete(0, END)
    CuadroApellido.delete(0, END)
    CuadroDireccion.delete(0, END)
    # usamos el método consultado .delete(inicio, fin) para borrar de manera eficiente el campo requerido


# barra menú----------------------------------------------------------------------------
BarraMenu = Menu (root)
root.config(menu= BarraMenu)
# menú archivos-------------------------------------------------------------------------
ArchivoBBDD = Menu(BarraMenu)
ArchivoBorrar = Menu(BarraMenu)
ArchivoCRUD = Menu(BarraMenu)
ArchivoAyuda = Menu(BarraMenu)
# sub-menús-----------------------------------------------------------------------------

ArchivoBBDD = Menu(BarraMenu, tearoff= 0)                                      # menú principal
ArchivoBBDD.add_command(label= "Conectar", command= infoConectar)              # sub menú
ArchivoBBDD.add_command(label= "Salir", command = root.quit)

ArchivoBorrar = Menu(BarraMenu, tearoff= 0)                                    # menú principal
ArchivoBorrar.add_command(label= "Borrar campos", command= infoBorrar)                              # sub menú

ArchivoCRUD = Menu(BarraMenu, tearoff= 0)                                      # menú principal
ArchivoCRUD.add_command(label= "Crear", command= Crear_Registro)               # sub menú
ArchivoCRUD.add_command(label= "Leer", command= Leer_Registro)
ArchivoCRUD.add_command(label= "Actualizar", command= Actualizar_Registro)
ArchivoCRUD.add_command(label= "Eliminar", command= Eliminar_Registro)

ArchivoAyuda = Menu(BarraMenu, tearoff= 0)                                     # menú principal
ArchivoAyuda.add_command(label= "Licencia", command= infoLicencia)             # sub menú
ArchivoAyuda.add_command(label= "Acerca de...", command= infoAcercaDe)        
# texto a la opción de menú y submenús---------------------------------------------------
BarraMenu.add_cascade(label= "BBDD", menu= ArchivoBBDD)                        # añadir texto usando add_cascade(), con los parámetros label y Menu
BarraMenu.add_cascade(label= "Borrar", menu= ArchivoBorrar)
BarraMenu.add_cascade(label= "CRUD", menu= ArchivoCRUD)
BarraMenu.add_cascade(label= "Ayuda", menu= ArchivoAyuda)


# entrys--------------------------------------------------------------------------------
CuadroID = Entry(MiFrame)
CuadroID.grid(row= 0, column=1, padx= 10, pady= 10, columnspan= 3)
CuadroID.config(justify= "center")

CuadroNombre = Entry(MiFrame)
CuadroNombre.grid(row= 1, column=1, padx= 10, pady= 10, columnspan= 3)
CuadroNombre.config(justify= "center")

CuadroPassword = Entry(MiFrame)
CuadroPassword.grid(row= 2, column=1, padx= 10, pady= 10, columnspan= 3)
CuadroPassword.config(justify= "center", show= "*")

CuadroApellido = Entry(MiFrame)
CuadroApellido.grid(row= 3, column=1, padx= 10, pady= 10, columnspan= 3)
CuadroApellido.config(justify= "center")

CuadroDireccion = Entry(MiFrame)
CuadroDireccion.grid(row= 4, column=1, padx= 10, pady= 10, columnspan= 3)
CuadroDireccion.config(justify= "center")

#CuadroComentarios = Entry(MiFrame)
#CuadroComentarios.grid(row= 5, column=1, padx= 20, pady= 20)
#CuadroComentarios.config(justify= "center")

# labels---------------------------------------------------------------------------------
IdLabel = Label(MiFrame, text= "ID: ")
IdLabel.grid(row= 0, column= 0, sticky= "e")

NombreLabel = Label(MiFrame, text= "Nombre: ")
NombreLabel.grid(row= 1, column= 0, sticky= "e")

PasswordLabel = Label(MiFrame, text= "Password: ")
PasswordLabel.grid(row=2, column= 0, sticky= "e")

ApellidoLabel = Label(MiFrame, text= "Apellido: ")
ApellidoLabel.grid(row= 3, column= 0, sticky= "e")

DireccionLabel = Label(MiFrame, text= "Dirección: ")
DireccionLabel.grid(row= 4, column= 0, sticky= "e")

#ComentariosLabel = Label(MiFrame, text= "Comentarios: ")
#ComentariosLabel.grid(row=5, column=0, sticky= "e")

# botones funcionales--------------------------------------------------------------------
botonCreate = Button(MiFrame, text= "Create", command= Crear_Registro)
botonCreate.grid(row= 5, column= 1, padx= 5, pady= 5)

botonRead = Button(MiFrame, text= "Read", command= Leer_Registro)
botonRead.grid(row= 5, column= 2, padx= 5, pady= 5)

botonUpdate = Button(MiFrame, text= "Update", command= Actualizar_Registro)
botonUpdate.grid(row= 5, column= 3, padx= 5, pady= 5)

botonDelete = Button(MiFrame, text= "Delete", command= Eliminar_Registro)
botonDelete.grid(row= 5, column= 4, padx= 5, pady= 5)


root.mainloop()