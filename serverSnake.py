import socket, threading, sys

jugadoresOnline = [[]]
areasDisponibles =[[0,0],[310,0],[0,310],[310,310]]
coloresDisponibles =[[199,0,57],[27,227,106],[245,187,4],[32,229,16]]

class hilo_server(threading.Thread): #Hilo e instrucciones
    def __init__(self,conexion,dir,jugadores):
        threading.Thread.__init__(self)
        self.conexion = conexion
        self.dir = dir
        self.jugadores = jugadores

    def transmitir(self,dt):
        for jugador in self.jugadores:
            try:            
                instruccion = "\n"+self.dir[0]+": "+ dt
                jugador.send(instruccion.encode())
            except Exception as e:
                continue

    def run(self):
        print("\nNueva conexion:",self.dir[0])
        while True:
            dato = self.conexion.recv(2048)
            dt = dato.decode()
            for jugador in jugadoresOnline():
                if jugador[1] == self.dir:
                    print()
            if dt == "":
                continue
            print(self.dir[0]," > ",dt)
            self.transmitir(dt)

class servidor(): #Crear e Iniciar Servidor
    nJugadores = 1
    server="" #Direccion con la que se iniciara el server
    def asigjugadores(self,numero):
        self.njugadores = numero

    def asigIPugadores(self,ip):
        self.server = ip

    def iniciar(self,):
        hilos =[]
        """
        socket_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        socket_server.connect(("8.8.8.8", 80))
        server = socket_server.getsockname()[0]
        socket_server.close
        """
        socket_server = socket.socket()
        try:
            socket_server.bind((self.server,3000))
        except socket.error as e:
            str(e)

        socket_server.listen(self.njugadores)

        print("\nSocket iniciado:\n Esperando conexiones")
        while True:
            conexion,dir = socket_server.accept()
            jugadoresOnline.append([conexion,dir])
            print("\nConexion: ",dir[0])
            hilo = hilo_server(conexion,dir,jugadoresOnline)
            hilo.start()
            hilos.append(hilo)

servidor.iniciar()