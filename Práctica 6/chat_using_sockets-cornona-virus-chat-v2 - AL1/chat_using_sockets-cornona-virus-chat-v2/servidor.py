import socket
import threading
import sys
import pickle
import os

class Servidor():
	# Función para crear y blindear el socket con el clinte, crear un hilo para aceptar mensajes y otro para procesar mensajes, crear un array de almacenamiento de clientes conectador y desplegar la opción de salir del programa  
	def __init__(self, host=socket.gethostname(), port=int(input("Que puerto quiere usar ? "))):
		
        ##Lista de clientes conectados
		self.clientes = []
        ####Lista de nicknames de clientes conectados
		self.nicknamesConectados = []

		print('\nSu IP actual es : ',socket.gethostbyname(host))
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(), '\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		self.s = socket.socket()
		self.s.bind((str(host), int(port)))
		self.s.listen(30)
		self.s.setblocking(False)

		threading.Thread(target=self.aceptarC, daemon=True).start()
		threading.Thread(target=self.procesarC, daemon=True).start()

		while True:

			## Mostrará los nickname de los usuarios conectados al servidor en ese intante
			print('\nUsuarios conectados:\n')
			for c in self.nicknamesConectados:
				print(self.nicknamesConectados)

			msg = input('\n << SALIR = 1 >> \n')

			if msg == '1':
				print(" **** Me piro vampiro; cierro socket y mato SERVER con PID = ", os.getpid())
				self.s.close()
				sys.exit()
			else: pass

    # Función que abre el documento de texto(u22060943AI1.txt") y añade, con el metodo append, al final del docuemnto los mensajes enviados              
	def guardarHistorialChat(self, msg):
		f=open("u22060943AI1.txt", "a")
		f.write(msg + "\n")
		f.close()

	# Función que recibe en el socket a los clientes, que con la función connect() en el lado del cliente, y los acepta la conexión. 
	def aceptarC(self):
		print('\nHilo ACEPTAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		
		while True:
			try:
				conn, addr = self.s.accept()
				print(f"\nConexion aceptada via {addr}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
			except: pass

	# Función que recorre la lista de clientes activos para recibir todo lo enviado por los clientes y posteriormente llamar a la funcion broadcast
	def procesarC(self):
		print('\nHilo PROCESAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(32)
						if '~' in data:
							nickname=pickle.loads(data)
							self.nicknamesConectados.append(nickname.replace('~',''))
							##Se recibe el nickname, identificado gracias al caracter añadido al enciar '~', caracter eliminado posteriormente con la función replace
                            ## Al final de la lista de nicknames, el nuevo nickanme recibido del nuevo cliente que se conecta al servidor, es añadido
						else:
							self.broadcast(data,c)
							self.guardarHistorialChat(data)
						 	### Se envia el mensaje a los clientes con la función broadcast y se envian los mensajes al fichero de texto con la funcion guardarHistorialChat para almacenarlos en este
					except: pass
	# Función para enviar a todos los clientes conecatdos al servidor el mensaje a excepción del emisor
	def broadcast(self, msg, cliente):
		for c in self.clientes:
			print("Clientes conectados Right now = ", len(self.clientes))
			try:
				if c != cliente: 
					print(pickle.loads(msg))
					c.send(msg)
			except: self.clientes.remove(c)

arrancar = Servidor() 