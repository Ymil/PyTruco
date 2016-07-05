'''
Programa de ejecucion del servidor PyTruco
16-01-2015
Lautaro Linquiman
'''

import logging

logging.basicConfig(format='%(levelname)s [%(asctime)s][SVR]: %(message)s',filename='../logs/servidor.log')
import cservidor
import traceback
import threading
import sys
from time import sleep
try:
	import gtk
	InterfaceGrafica = 0
except:
	InterfaceGrafica = 0
if(InterfaceGrafica):
	class app:
		def __init__(self):

			self.conectado = 0
			self.conexion = 0

			self.ventana = gtk.Window()
			self.ventana.set_title('Servidor PyTruco - Espera')
			self.ventana.set_default_size(350,80)
			self.ventana.connect('destroy', self.exit)

			vBox = gtk.VBox()
			self.ventana.add(vBox)

			hBox1 = gtk.HBox()
			hBox2 = gtk.HBox()
			hBox3 = gtk.HBox()

			vBox.pack_start(hBox1, 0, 0, 0)
			vBox.pack_start(hBox2, 0, 0, 0)
			vBox.pack_start(hBox3, 0, 0, 0)

			lIP = gtk.Label('IP')
			lPort = gtk.Label('Puerto')

			self.inputIP = gtk.Entry()
			self.inputIP.set_text('localhost')

			self.inputPort = gtk.Entry()
			self.inputPort.set_text('9999')

			hBox1.pack_start(lIP, 1, 5, 0)
			hBox2.pack_start(lPort, 1, 5, 0)
			hBox1.pack_end(self.inputIP, 0, 5, 0)
			hBox2.pack_end(self.inputPort, 0, 5, 0)

			bottonConectar = gtk.Button('Conectar')
			bottonConectar.connect('clicked', self.conectar)

			hBox3.pack_start(bottonConectar,1,0,0)

			self.ventana.show_all()

			gtk.main()
		def desconectar(self):
			if(self.conexion == 1):
				self.conexion.desconectar()

		''' Eventos '''
		def exit(self, widget):
			gtk.main_quit()
			exit()

		def conectar(self, widget):
			if(self.conectado == 0):
				config = {'ip':'','port':0}
				config['ip'] = self.inputIP.get_text()
				config['port'] = int(self.inputPort.get_text())
				self.conexion = cservidor.servidor(config)
				thread = threading.Thread(target=self.conexion.conectar)
				thread.start()
				sleep(1)
				if(self.conexion.getStatusConection() == 1):
					self.ventana.set_title('Servidor PyTruco - Funcionando')
					widget.set_label('Desconectar')
					self.conectado = 1
				else:
					self.show_dialog()
			else:
				self.conexion.desconectar()
				widget.set_label('Conectar')
				self.conectado = 0
				self.ventana.set_title('Servidor PyTruco - Detenido')

		''' dialogos '''
		def show_dialog(self):
			buttons = (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
			dialog = gtk.Dialog(title='Error: IP ocupada',
								parent=self.ventana,
								flags = 0,
								buttons = buttons)
			image = gtk.Image()
			image.set_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_DIALOG)

			lError = gtk.Label('La ip que utilizas ya esta ocupada')

			hBox = gtk.HBox()
			hBox.pack_start(image, 0, 0, 2)
			hBox.pack_end(lError, 1, 1, 2)
			dialog.vbox.pack_start(hBox)
			hBox.show_all()
			response = dialog.run()
			dialog.destroy()



	aplicacion = app()
