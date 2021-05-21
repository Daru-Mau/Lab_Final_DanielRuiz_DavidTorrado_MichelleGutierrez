import socket, threading, sys

jugadoresOnline = [[]]
coloresUsados =[[]]

class hilo_server(threading.Thread):
    def __init__(self,conexion,dir,jugadores):
        threading.Thread.__init__(self)
        self.conexion = conexion
        self.dir = dir
        self.jugadores = jugadores

    def transmitir(self,dt):
        for jugador in self.jugadores:
            try:            
                mensaje = "\n"+self.dir[0]+": "+ dt
                jugador.send(mensaje.encode())
            except Exception as e:
                continue

    def run(self):
        print("\nNueva conexion:",self.dir[0])
        while True:
            dato = self.conexion.recv(2048)
            dt = dato.decode()
            if dt == "":
                continue
            print(self.dir[0]," > ",dt)
            self.transmitir(dt)

class servidor():
    def iniciar():
        hilos =[]
        server=""
        socket_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        socket_server.connect(("8.8.8.8", 80))
        server = socket_server.getsockname()[0]
        socket_server.close
        socket_server = socket.socket()
        try:
            socket_server.bind((server,3000))
        except socket.error as e:
            str(e)

        socket_server.listen(4)

        print("\nSocket iniciado:\n Esperando conexiones")
        while True:
            conexion,dir = socket_server.accept()
            jugadoresOnline.append(conexion)
            print("\nConexion: ",dir[0])
            hilo = hilo_server(conexion,dir,jugadoresOnline)
            hilo.start()
            hilos.append(hilo)

servidor.iniciar()