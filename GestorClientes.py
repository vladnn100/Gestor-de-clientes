#importando librerias
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()

#Posicionando la ventana en el centro
ancho_ventana = 600
alto_ventana = 245

x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2

posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
root.geometry(posicion)
root.config(bg="powder blue")

root.resizable(0,0)

#Colocando titulo a mi ventana
root.title('Gestor de clientes')

#Creando la concexión a la base de datos
conn = sqlite3.connect('microCRM.db')

#Creando el cursor para las operaciones de base de datos
c = conn.cursor()

#Ejecutando consulta para crear nuestra tabla
c.execute("""
			CREATE TABLE if not exists cliente (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				nombre TEXT NOT NULL,
				telefono TEXT NOT NULL,
				empresa TEXT NOT NULL
			);
""")

#Creando la funcion para mostrar los clientes y sus datos
def render_clientes():
	rows = c.execute("SELECT * FROM cliente").fetchall()

	#Eliminando los datos en la tabla antes de renderizarlos nuevamente
	tree.delete(*tree.get_children())

	for row in rows:
		tree.insert('', END, row[0], values=(row[1], row[2], row[3]))

#Creando la funcion para insertar los clientes y sus datos
def insertar(cliente):
	c.execute("""
			INSERT INTO cliente(nombre, telefono, empresa) VALUES (?, ?, ?)
			""", (cliente['nombre'], cliente['telefono'], cliente['empresa']))
	conn.commit()

	#Mostrar los clientes y sus datos 
	render_clientes()

#Definiendo la funcion nuevo cliente
def nuevo_cliente():

	#Creando la funcion "guardar"
	def guardar():

		#Creando validaciones para las entradas de "Nuevo cliente"
		if not nombre.get():
			messagebox.showerror('Error','El nombre es obligatorio')
			return
		if not telefono.get():
			messagebox.showerror('Error','El telefono es obligatorio')
			return
		if not empresa.get():
			messagebox.showerror('Error','La empresa es obligatoria')
			return

		#Guardando valores en mi diccionario
		cliente = {
			'nombre': nombre.get(),
			'telefono': telefono.get(),
			'empresa': empresa.get()
		}

		#Llamando la funcion insertar
		insertar(cliente)

		#Cerrando ventana "Nuevo cliente"
		top.destroy()

	#Creando ventana "Nuevo cliente"
	top = Toplevel()

	#Posicionando la ventana en la parte superior del centro
	ancho_ventana = 300
	alto_ventana = 100

	x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
	y_ventana = root.winfo_screenheight() // 2 - alto_ventana * 3

	posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
	top.geometry(posicion)
	top.config(bg="powder blue")

	top.title('Nuevo cliente')

	#Creando y customizando etiquetas y entradas de la ventana "Nuevo cliente"
	lnombre = Label(top, text='Nombre', bg="powder blue")
	nombre = Entry(top, width=40)
	lnombre.grid(row=0, column=0)
	nombre.grid(row=0, column=1)

	ltelefono = Label(top, text='Teléfono', bg="powder blue")
	telefono = Entry(top, width=40)
	ltelefono.grid(row=1, column=0)
	telefono.grid(row=1, column=1)

	lempresa = Label(top, text='Empresa', bg="powder blue")
	empresa = Entry(top, width=40)
	lempresa.grid(row=2, column=0)
	empresa.grid(row=2, column=1)

	#Creando boton de "Guardar"
	guardar = Button(top, text='Guardar', command=guardar, bg="light steel blue")
	guardar.grid(row=3, column=1)

	#Comando para que quede en espera
	top.mainloop()

#Creando la funcion para insertar los clientes y sus datos
def eliminar_cliente():
	id = tree.selection()[0]

	#Trayendo los datos del cliente
	cliente = c.execute("SELECT * FROM cliente WHERE id = ?", (id, )).fetchone()

	#Creando validaciones para confirmar la eliminación de un cliente
	respuesta = messagebox.askokcancel('Seguro?', 'Estas seguro de querer eliminar el cliente ' + cliente[1] + '?')
	
	if respuesta:
		c.execute("DELETE FROM cliente WHERE id = ?", (id, ))
		conn.commit()

		#Mostrar los clientes y sus datos
		render_clientes()

	else:
		pass

#Creando el boton "Nuevo Cliente"
btn_agregar = Button(root, text='Nuevo Cliente', command=nuevo_cliente, bg="light steel blue")
btn_agregar.grid(column=0, row=0)

#Creando el boton "Eliminar Cliente"
btn_eliminar=Button(root, text='Eliminar cliente', command=eliminar_cliente, bg="light steel blue")
btn_eliminar.grid(column=1, row=0)

#Creando la tabla de los datos de clientes
tree = ttk.Treeview(root)

#Cambiar de color a los encabezados de la tabla
style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview.Heading", background="azure", foreground="black")

tree['columns'] = ('Nombre','Telefono','Empresa')

tree.column('#0', width=0, stretch=NO)
tree.column('Nombre')
tree.column('Telefono')
tree.column('Empresa')

#Customizando la tabla de datos de clientes
tree.heading('Nombre', text='Nombre')
tree.heading('Telefono', text='Telefono')
tree.heading('Empresa', text='Empresa')
tree.grid(column=0, row=1, columnspan=2)

#Mostrar los clientes y sus datos
render_clientes()

#Comando para que quede en espera
root.mainloop()

