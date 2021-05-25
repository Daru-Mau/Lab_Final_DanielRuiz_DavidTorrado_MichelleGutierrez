import socket, threading,pickle

class Hilo_Partida(threading.Thread): #Hilo e instrucciones
    def __init__(self,conexion,dir,cliente):
        threading.Thread.__init__(self)
        self.conexion = conexion
        self.dir = dir
        self.jugadores = cliente.jugadoresOnline
        self.limite = cliente.esperandoJugadores
        self.posIni = cliente.zonasDisponibles[len(self.jugadores)-1]
        print(self.posIni)
        self.color = cliente.coloresDisponibles[len(self.jugadores)-1]
        print(self.color)


    def transmitir(self,dt):
        """[summary] Funcion encargada de transmitir una accion a todos los jugadores conectados

        Args:
            dt ([String]): [description]
        """
        for jugador in self.jugadores:
            try:            
                instruccion = dt
                jugador.send(instruccion.encode())
            except Exception as e:
                continue

    def run(self):
        print("\nNueva conexion:",self.dir[0])
        while len(self.jugadores) < self.limite:
            self.transmitir(str(self.jugadores))
        self.transmitir("comenzar")
        print("El juego puede comenzar")
        self.transmitir(pickle.dumps([self.posIni,self.color]))
        while True:
            try:
                dato = self.conexion.recv(2048)
                dt = dato.decode()
                if dt == "":
                    continue
                print(self.dir[0],": ",dt)
                self.transmitir(dt)
            except Exception as e:
                continue

class Servidor(): #Crear e Iniciar Servidor

    def asigIPjugadores(self,ip):
        self.host = ip

    def iniciar(self):
        self.jugadoresOnline = []
        self.zonasDisponibles =[[0,0],[310,0],[0,310],[310,310]]
        self.coloresDisponibles =[[199,0,57],[27,227,106],[245,187,4],[32,229,16]]
        self.esperandoJugadores = 0
        hilos =[]
        host="localhost" #Direccion con la que se iniciara el server
        """
        socket_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        socket_server.connect(("8.8.8.8", 80))
        server = socket_server.getsockname()[0]
        socket_server.close
        """
        socket_server = socket.socket()
        try:
            socket_server.bind((host,3000))
        except socket.error as e:
            str(e)
        socket_server.listen(4)
        print("\nSocket iniciado:\n Esperando conexiones")
        while True:
            conexion,dir = socket_server.accept()
            if self.esperandoJugadores == 0:
                self.esperandoJugadores = int(conexion.recv(2048).decode())
                print("numero de jugadores a esperar: ", self.esperandoJugadores)
            self.jugadoresOnline.append([conexion,dir])
            hilo = Hilo_Partida(conexion,dir,self)
            hilo.start()
            hilos.append(hilo)
server = Servidor()
server.iniciar()