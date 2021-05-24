import socket, threading,pickle

jugadoresOnline = [[]]
zonasDisponibles =[[0,0],[310,0],[0,310],[310,310]]
coloresDisponibles =[[199,0,57],[27,227,106],[245,187,4],[32,229,16]]

class hilo_server(threading.Thread): #Hilo e instrucciones
    def __init__(self,conexion,dir,jugadores,posInicial,color):
        threading.Thread.__init__(self)
        self.conexion = conexion
        self.dir = dir
        self.posIni = posInicial
        self.color = color
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
        if len(jugadoresOnline) ==4:
            self.transmitir("comenzar".encode())
        while True:
            snake_pos=0,0 #Temporal
            dato = self.conexion.recv(2048)
            dt = pickle.loads(dato)
            if dt == "":
                continue
            if dt == "RIGHT":
                snake_pos[0]+=10
            if dt == "LEFT":
                snake_pos[0]-=10
            if dt == "UP":
                snake_pos[1]-=10
            if dt == "DOWN":
                snake_pos[1]+=10
            print(self.dir[0],": ",dt)
            self.transmitir(pickle.dumps(snake_pos))

class servidor(): #Crear e Iniciar Servidor
    def asigjugadores(self,numero):
        self.njugadores = numero
    def asigIPjugadores(self,ip):
        self.host = ip

    def iniciar():
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
            jugadoresOnline.append([conexion,dir])
            print("\nConexion: ",dir[0])
            hilo = hilo_server(conexion,dir,jugadoresOnline,zonasDisponibles[len(jugadoresOnline)],coloresDisponibles[0])
            hilo.start()
            hilos.append(hilo)

servidor.iniciar()