from imutils.video import VideoStream
from pyzbar import pyzbar
from datetime import datetime
from tabulate import tabulate
import imutils
import time
import math
import qrcode
import random 
import sys
import cv2
import serial


# librerias postgresql
import psycopg2

#Constantes Globales
PSQL_HOST = 'localhost'
PSQL_PORT = '5432'
PSQL_USER = 'postgres'
PSQL_PASS = '46758648'
PSQL_DB = 'electronica'

pines = list()
ser = serial.Serial('COM3',9600 ,timeout = None)
time.sleep(2)
# CONEXION 
direccion_conexion = """
host=%s port=%s user=%s password=%s dbname=%s"""% (PSQL_HOST,PSQL_PORT,PSQL_USER,PSQL_PASS,PSQL_DB)
conexion = psycopg2._connect(direccion_conexion)
cursor = conexion.cursor()

#Parametros iniciales 

#Actualizacion 
sql_p_in = """UPDATE equipo SET p_in = %s WHERE nombre = %s"""

def Ingreso(carne):
	intentos_p = 0
	cursor.execute('SELECT * FROM alumnos WHERE carne=%s;' %(carne))
	valores = cursor.fetchall()
	print('valores',valores)
	usuario_trabajo = valores[0]
	print(usuario_trabajo)
	print('Se a confirmado el usuario : ',usuario_trabajo[1])
	while(intentos_p <= 3):
		ser.write(str('eee').encode("utf-8"))
		print('Digite su PIN: ')
		#LECTURA DE MATRIZ ARDUINO
		pin_escrito = int(ser.readline().decode('ascii'))
		if pin_escrito == usuario_trabajo[6]:
			print('USUARIO AUTENTICADO EXITOSAMENTE.....')
			print('-----------------------------------------------')
			#Actualizar en la tabla de alumnos columna ingreso
			hora_entrada = str(datetime.now())
			sql="UPDATE alumnos SET f_in = %s WHERE alumno_id = %s "
			datos = (hora_entrada, usuario_trabajo[0],)
			cursor.execute(sql, datos)
			conexion.commit()

			print('Se a registrado su entrada exitosamente')
			print('Nombre: %s' % (usuario_trabajo[1],))
			print('Carne: %s' % (usuario_trabajo[2],))
			print('Hora de entrada: %s' % (hora_entrada,))
			print('ADELANTE...........')
			#Muestra final de la tabla equipo
			print('-----------------------------------------------')
			ser.write(str('eeee').encode("utf-8"))
			time.sleep(1.0)
			ser.write(str('eeee').encode("utf-8"))
			time.sleep(1.0)
			ser.write(str('eeee').encode("utf-8"))
			time.sleep(1.0)
			ser.write(str('eeee').encode("utf-8"))
			time.sleep(1.0)

			print('-----------------------------------------------')
			seleccion = 0
			break
		else:
			print('PIN INCORRECTO!!!!!, solo tienes 4 intentos')
			intentos_p = intentos_p + 1
			print('Intentos usados: ', intentos_p)
			print('-----------------------------------------------')

def salida(carne):
	intentos_s = 0
	cursor.execute('SELECT * FROM alumnos WHERE carne=%s;' %(carne))
	valores = cursor.fetchall()
	print('valores',valores)
	usuario_trabajo = valores[0]
	print(usuario_trabajo)
	print('Se a confirmado el usuario : ',usuario_trabajo[1])

	while(intentos_s<= 3):
		ser.write(str('eee').encode("utf-8"))
		print('Digite su PIN: ')
		#LECTURA DE MATRIZ ARDUINO
		pin_escrito = int(ser.readline().decode('ascii'))
		if pin_escrito == usuario_trabajo[6]:
			print('USUARIO AUTENTICADO EXITOSAMENTE.....')
			print('-----------------------------------------------')
			#Actualizar en la tabla de alumnos columna ingreso
			hora_salida = str(datetime.now())
			#Actualizar en la tabla de alumnos fecha de salida
			sql="UPDATE alumnos SET f_out = %s WHERE alumno_id = %s "
			datos = (hora_salida, usuario_trabajo[0],)
			cursor.execute(sql, datos)
			conexion.commit()

			print('Se a registrado su entrada exitosamente')
			print('Nombre: %s' % (usuario_trabajo[1],))
			print('Carne: %s' % (usuario_trabajo[2],))
			print('Hora de entrada: %s' % (hora_salida,))
			print('QUE TE VAYA BIEN!...........')
			print('-----------------------------------------------')
			ser.write(str('eeee').encode("utf-8"))
			time.sleep(1.0)
			ser.write(str('eeee').encode("utf-8"))
			time.sleep(1.0)
			ser.write(str('eeee').encode("utf-8"))
			time.sleep(1.0)
			ser.write(str('eeee').encode("utf-8"))
			time.sleep(1.0)
	
			print('-----------------------------------------------')
			seleccion = 0;
			break
		else:
			print('PIN INCORRECTO!!!!!, solo tienes 4 intentos')
			intentos_s = intentos_s + 1
			print('Intentos usados: ', intentos_s)
			print('-----------------------------------------------')			

def NewUser(nombre,carne):
	cursor.execute('SELECT * FROM alumnos;')
	valores = cursor.fetchall()
	longitud = len(valores)
	new_pin = random.randint(111111,999999)
	for i in range(0,longitud):
		lista = valores[i]
		pin = str(lista[6])
		pines.append(pin)			
		i += 1
	for j in range(len(pines)):
		if new_pin == lista[i]:
			print("El Pin ya existe")
			new_pin = random.randint(111111,999999)
			break
		else:
			print("El pin para el usuario nuevo es: ")
			print(new_pin)

			break	
	print("el pin para el usuario %s es %s: " % (nombre, new_pin))
	sql="INSERT INTO alumnos(nombre_a,carne,pin) VALUES (%s,%s,%s)"
	datos = (nombre,carne,new_pin)
	cursor.execute(sql, datos)
	conexion.commit()
	print('Usuario guardado exitosamente: ')
	cursor.execute('SELECT * FROM alumnos WHERE carne = %s;' %(carne,))
	nuevo_usuario_lista = cursor.fetchall()
	nuevo_usuario = nuevo_usuario_lista[0]
	print('Nombre: %s' % (nuevo_usuario[1],))
	print('Carne: %s' % (nuevo_usuario[2],))
	print('PIN: %s' % (nuevo_usuario[6],))
	print('a continuacion se creara el codigo QR para el usuario')
	dato = carne
	qr_img = qrcode.make(dato)  
	#f = open("%s.png", "wb" %(nombre,))
	f = str(carne+'.jpg')
	qr_img.save(f)
	img = cv2.imread("%s" % (f,))
	cv2.imshow("Codigo QR", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	print('-----------------------------------------------')

def NewEquipment():
	EquipName = input('Ingrese el nombre del equipo: ')
	EquipStock = input('Ingrese el stock del equipo:  ')
	sql="INSERT INTO equipo(nombre,stock) VALUES (%s,%s)"
	datos = (EquipName,EquipStock)
	cursor.execute(sql, datos)
	conexion.commit()
	print('Se Agrego el nuevo equipo Satisfactoriamente')
	#Muestra final de la tabla equipo
	cursor.execute('SELECT * FROM equipo;')
	equipo = cursor.fetchall()
	print('ID        Nombre         Stock')
	print(tabulate(equipo))
	print('-----------------------------------------------')

def prestamo(carne):
	intentos_p = 0
	cursor.execute('SELECT * FROM alumnos WHERE carne=%s;' %(carne))
	valores = cursor.fetchall()
	print('valores',valores)
	usuario_trabajo = valores[0]
	print(usuario_trabajo)
	print('Se a confirmado el usuario : ',usuario_trabajo[1])

	

	while(intentos_p <= 3):
		ser.write(str('eee').encode("utf-8"))
		print('Digite su PIN: ')
		#LECTURA DE MATRIZ ARDUINO
		pin_escrito = int(ser.readline().decode('ascii'))
		if pin_escrito == usuario_trabajo[6]:
			print('USUARIO AUTENTICADO EXITOSAMENTE.....')
			print('-----------------------------------------------')
			cursor.execute('SELECT * FROM equipo;')
			equipo = cursor.fetchall()
			print('ID        Nombre         Stock')
			print(tabulate(equipo))
			hora_prestamo = str(datetime.now())
			ser.write(str('ee').encode("utf-8"))
			print('Ingrese el id del equipo a prestar: ')
			id_equipo = int(ser.readline().decode('ascii'))
			#Seleccion del equipo

			cursor.execute('SELECT * FROM equipo WHERE equipo_id = %s;' %(id_equipo,))
			equipo_lista = cursor.fetchall()
			equipo_trabajo = equipo_lista[0]
			print(equipo_trabajo)
			#Insertar en la tabla de prestamos el nuevo prestamo

			sql="INSERT INTO prestamos(alumno_id, p_in, equipo_id) VALUES (%s,%s,%s)"
			datos = (usuario_trabajo[0], hora_prestamo, id_equipo)
			cursor.execute(sql, datos)
			conexion.commit()
			#Update tabla alumnos Para saber que equipo tiene que alumno

			sql="UPDATE alumnos SET equipo_id = %s WHERE nombre_a = %s"
			datos = (id_equipo, usuario_trabajo[1])
			cursor.execute(sql, datos)
			conexion.commit()
			#Update stock de equipo

			nuevo_stock = int(equipo_trabajo[2]) - 1
			nuevo_stock_str = str(nuevo_stock)
			sql="UPDATE equipo SET stock = %s WHERE equipo_id = %s"
			datos = (nuevo_stock_str, id_equipo)
			cursor.execute(sql, datos)
			conexion.commit()
			#mensajes finales

			print('Prestamo Realizado con exito')
			print('Nombre: %s' % (usuario_trabajo[1],))
			print('Carne: %s' % (usuario_trabajo[2],))
			print('Equipo Prestado: %s' % (equipo_trabajo[1]))
			print('Hora de prestamo: %s' % (hora_prestamo,))
			print('Stock Restante : %s' % (nuevo_stock_str,))
			#Muestra final de la tabla equipo

			cursor.execute('SELECT * FROM equipo;')
			equipo = cursor.fetchall()
			print('ID        Nombre         Stock')
			print(tabulate(equipo))
			print('-----------------------------------------------')
			break
		else:
			print('PIN INCORRECTO!!!!!, solo tienes 4 intentos')
			intentos_p = intentos_p + 1
			print('Intentos usados: ', intentos_p)
			print('-----------------------------------------------')

def devolucion(carne):
	intentos_d = 0
	cursor.execute('SELECT * FROM alumnos WHERE carne=%s;' %(carne))
	valores = cursor.fetchall()
	print('valores',valores)
	usuario_trabajo = valores[0]
	print(usuario_trabajo)
	print('Se a confirmado el usuario : ',usuario_trabajo[1])

	while(intentos_d <= 3):
		ser.write(str('eee').encode("utf-8"))
		print('Digite su PIN: ')
		pin_escrito_d = int(ser.readline().decode('ascii'))
		if pin_escrito_d == usuario_trabajo[6]:
			cursor.execute('SELECT * FROM equipo;')
			equipo = cursor.fetchall()
			print('ID        Nombre         Stock')
			print(tabulate(equipo))
			hora_devolucion = str(datetime.now())
			ser.write(str('ee').encode("utf-8"))
			print('Ingrese el id del equipo a devolver: ')
			id_equipo = int(ser.readline().decode('ascii'))
			#Seleccion del equipo

			cursor.execute('SELECT * FROM equipo WHERE equipo_id = %s;' %(id_equipo,))
			equipo_lista = cursor.fetchall()
			equipo_trabajo = equipo_lista[0]
			print(equipo_trabajo)
			#Actualizar en la tabla de prestamos la fecha de devolucion
			cursor.execute('SELECT prestamo_id FROM prestamos WHERE p_out IS NULL AND alumno_id = %s AND equipo_id = %s;' %(usuario_trabajo[0],equipo_trabajo[0],))
			prestamo_id = cursor.fetchall()
			print(prestamo_id)
			print(usuario_trabajo[0])
			sql="UPDATE prestamos SET p_out = %s WHERE equipo_id = %s AND prestamo_id = %s"
			datos = (hora_devolucion, id_equipo,prestamo_id[0],)
			cursor.execute(sql, datos)
			conexion.commit()


			#Update stock de equipo
			nuevo_stock = int(equipo_trabajo[2]) + 1
			nuevo_stock_str = str(nuevo_stock)
			sql="UPDATE equipo SET stock = %s WHERE equipo_id = %s"
			datos = (nuevo_stock_str, id_equipo)
			cursor.execute(sql, datos)
			conexion.commit()
			#mensajes finales

			print('Prestamo Realizado con exito')
			print('Nombre: %s' % (usuario_trabajo[1],))
			print('Carne: %s' % (usuario_trabajo[2],))
			print('Equipo Devuelto: %s' % (equipo_trabajo[1]))
			print('Hora de devolucion: %s' % (hora_devolucion,))
			print('Stock Restante : %s' % (nuevo_stock_str,))
			#Muestra final de la tabla equipo

			cursor.execute('SELECT * FROM equipo;')
			equipo = cursor.fetchall()
			print('ID        Nombre         Stock')
			print(tabulate(equipo))
			cursor.execute('SELECT * FROM prestamos;')
			prestamos = cursor.fetchall()
			print('Tabla   De    Prestamos')
			print(tabulate(prestamos))
			print('-----------------------------------------------')
			break
		else:
			print('PIN INCORRECTO!!!!!, solo tienes 4 intentos')
			intentos_d = intentos_d + 1
			print('Intentos usados: ', intentos_d)
			print('-----------------------------------------------')

def Registro_Prestamos():
	cursor.execute('SELECT alumnos.nombre_a, alumnos.carne, alumnos.equipo_id, equipo.nombre FROM alumnos INNER JOIN equipo ON (alumnos.equipo_id=equipo.equipo_id)')
	registro_prestamos = cursor.fetchall()
	print('Nombre Alumno   Carne   Equipo_id   Nombre Equipo')
	print(tabulate(registro_prestamos))
	print('-----------------------------------------------')

def Registro_Devoluciones():
	cursor.execute('SELECT prestamos.alumno_id,prestamos.p_in,prestamos.p_out,equipo.nombre,alumnos.nombre_a FROM prestamos INNER JOIN equipo ON (prestamos.equipo_id=equipo.equipo_id) INNER JOIN alumnos ON(alumnos.alumno_id=prestamos.alumno_id)')
	registro_devoluciones = cursor.fetchall()
	print('id_A -----fecha de prestamo ---- fecha de devolucion -------  equipo ------------- nombre  alumno')
	print(tabulate(registro_devoluciones))
	print('-----------------------------------------------')
	print('-------------------TABLA ALUMNOS---------------')
	cursor.execute('SELECT * FROM alumnos')
	registro_alumnos = cursor.fetchall()
	print(tabulate(registro_alumnos))
	print('-----------------------------------------------')



def lecturaQR():
	text=''
	print("[INFO] starting video stream...")
	vs = VideoStream(src=1).start()
	time.sleep(2.0)
	found = set()
	while True:
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
		barcodes = pyzbar.decode(frame)
		for barcode in barcodes:
			barcodeData = barcode.data.decode("utf-8")
			text = "{} ".format(barcodeData)
		if barcodes :
			break

	print("[INFO] cleaning up...")
	print('QR INFORMATION............')
	return text
	cv2.destroyAllWindows()
	vs.stop()
	print('-----------------------------------------------')

	
	

print('Bienvenido al sistema seleccione la opcion a utilizar: ')
while True:
	seleccion = 0
	if seleccion == 0:
		print('Opciones de el sistema')
		print('1. Ingresar al laboratorio')
		print('2. Nuevo Usuario') # Completo
		print('3. Nuevo Equipo') # Completo
		print('4. Prestamo de equipo') #union pin arduino
		print('5. Devolucion de equipo')#union pin arduino
		print('6. Registro de Prestamos Actuales')# Completo
		print('7. Registro de devoluciones y Alumnos')# Completo
		print('8. Salir del laboratorio')
		print('9. Salir de el sistema')
		print('Digite el valor de su seleccion: ')
		print('------------------------------------------')
		# Nuevo Usuario
		ser.write(str('le').encode("utf-8"))
		seleccion = int(ser.readline().decode('ascii'))
	if seleccion ==1:
		readQR = lecturaQR()
		Ingreso(readQR)
		seleccion=0

	elif seleccion == 2:
		name = input('Ingrese el nombre del alumno: ')
		carne = input('Ingrese el numero de carne: ')
		NewUser(name,carne)
	#Nuevo Equipo
	if seleccion == 3:
		NewEquipment()
	# Prestamo de Equipo
	elif seleccion == 4:
		readQR = lecturaQR()
		print(readQR)
		#time.sleep(1.0)
		prestamo(readQR)
	# Devolucion de equipo 
	elif seleccion == 5:
		readQR = lecturaQR()
		devolucion(readQR)
	#Registro de prestamos actuales, alumnos y equipos prestados
	elif seleccion == 6:
		Registro_Prestamos()
	elif seleccion == 7:
		Registro_Devoluciones()

	elif seleccion == 8:
		readQR = lecturaQR()
		salida(readQR)
	
	#SALIDA
	elif seleccion == 9:
		conexion.close()
		ser.close()
		cv2.destroyAllWindows()
		print('Se a cerrado todo exitosamente, Graciar por utilizar servicios Guerra! ')
		break

	else:
		seleccion = 0
		print('OPCION NO VALIDA!')
	time.sleep(2.0)
		
		
#conexion.close()
# close the output CSV file do a bit of cleanup
