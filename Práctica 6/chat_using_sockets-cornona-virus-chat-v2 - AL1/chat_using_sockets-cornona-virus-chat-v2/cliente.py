import threading
import sys
import socket
import pickle
import os

class Cliente():
	# Función para crear y conectar el socket, crear un hilo para recibir mensajes y desplegar un menu para selecionar entre salir del programa o mandar el mensaje 
	def __init__(self, host=input("Intoduzca la IP del servidor:  "), port=int(input("Intoduzca el PUERTO del servidor:  ")), nickname=input("Introduzca su correo electrónico de la universidad: ")):
					   #Se ingresa mediante el teclado la dirección ip del servidor y el puerto del servidor como los últimos 5 dígitos del expediente.
					   #Se ingresa mediante el teclado el correo electrónico de la universidad del cliente como parámatro de la función.

		self.s = socket.socket()
		self.s.connect((host, int(port)))
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		threading.Thread(target=self.recibir, daemon=True).start()

		while True:
			msg = input('\nEscriba texto ?   ** Enviar = ENTER   ** Salir Chat = 1 \n')
			if msg != '1' : self.enviar(nickname+" : "+msg)
			else:
				print(" **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid())
				self.s.close()
				sys.exit()

	# Función que recibe los mensajes y los imprime por pantalla
	def recibir(self):
		print('\nHilo RECIBIR con ID =',threading.currentThread().getName(), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			try:
				data = self.s.recv(32)
				if data: print(pickle.loads(data))
			except: pass

	# Función que envia los mensajes a traves de la red
	def enviar(self, msg):
		self.s.send(pickle.dumps(msg))

arrancar = Cliente()
#Revisión finalizada