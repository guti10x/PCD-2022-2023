import socket
import threading
import sys
import pickle
import os

class Servidor():

	def __init__(self, host=socket.gethostname(), port=int(input("Que puerto quiere usar ? "))):
		
		self.clientes = []
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

	def aceptarC(self):
		print('\nHilo ACEPTAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		
		while True:
			try:
				conn, addr = self.s.accept()
				print(f"\nConexion aceptada via {addr}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
			except: pass

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
							##Se añade al final de la lista de nicknames el nuevo nickanme recibido del nuevo cliente que se conecta al servidor 
						else:
							self.broadcast(data,c)
							self.guardarHistorialChat(data)
						 	### Se envia el mensaje a los clientes con la función broadcast y se envian los mensajes al fichero de texto con la funcion guardarHistorialChat para almacenarlos en este
					except: pass

	def broadcast(self, msg, cliente):
		for c in self.clientes:
			print("Clientes conectados Right now = ", len(self.clientes))
			try:
				if c != cliente: 
					print(pickle.loads(msg))
					c.send(msg)
			except: self.clientes.remove(c)

arrancar = Servidor() 