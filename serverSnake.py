import socket, threading, pickle

class Hilo_Partida(threading.Thread): #Hilo e instrucciones
    def __init__(self,conexion,dir,cliente):
        """[summary]
        Args:
            conexion ([type]): [description]
            dir ([type]): [description]
            cliente ([type]): [description]
        """
        threading.Thread.__init__(self)
        self.conexion = conexion        
        self.dir = dir
        self.jugadores = jugadoresOnline
        self.id = len(self.jugadores)
        self.limite = cliente.esperandoJugadores
        self.posIni = cliente.zonasDisponibles[len(self.jugadores)-1]
        self.color = cliente.coloresDisponibles[len(self.jugadores)-1]
        self.conexion.send(pickle.dumps([self.posIni,self.color,f"j{self.id}"]))

    def transmitir(self,dt):
        """[summary] Funcion encargada de transmitir una accion a todos los jugadores conectados
        Args:
            dt ([String]): [description]
        """
        global jugadoresOnline
        for jugador in jugadoresOnline:
            try: 
                jugador.send(f"{dt}".encode())
            except Exception as e:
                continue

    def run(self):
        """[summary]
        """
        global jugadoresOnline,puntajes,aceptando
        print("\nNuevo jugador:",self.dir[0]) 
        if len(jugadoresOnline) < self.limite:
            self.transmitir(self.limite-len(jugadoresOnline))
        elif len(jugadoresOnline) == self.limite:
            self.transmitir("comenzar")               
            while True:
                try:
                    dato = self.conexion.recv(2048)
                    dt = dato.decode()
                    print(dt)
                    if(dt != ""):
                        if "score" in dt:
                            puntajes.append(dt)
                            if len(puntajes)==len(jugadoresOnline):
                                puntajes.sort()
                                self.transmitir(f"ganador{puntajes[0]}")
                        #elif "posicion" in dt:
                            #dato = self.conexion.recv(2048)
                            #datos = pickle.loads(dato)
                        elif "salir" in dt:
                            jugadoresOnline.remove(self.conexion) 
                            puntajes.clear()                           
                            self.conexion.close()
                            aceptando = True
                            print("se aceptan mas jugadores")
                        else:
                            self.transmitir(dt)
                    else:
                        self.transmitir("")
                except Exception as e:
                    continue

jugadoresOnline = []
puntajes =[]
aceptando = True

class Servidor(): #Crear e Iniciar Servidor
    def asigIPjugadores(self,ip):
        self.host = ip
    def iniciar(self):
        global jugadoresOnline
        self.zonasDisponibles =[[0,0],[300,0],[0,300],[300,300]]
        self.coloresDisponibles =[[199,0,57],[27,227,106],[245,187,4],[32,229,16]]
        self.esperandoJugadores = 0
        hilos =[]
        host="26.19.70.130" #Direccion con la que se iniciara el server
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
        socket_server.listen()
        print("\nSocket iniciado:\n Esperando jugadores")
        global aceptando
        while True:
            try:
                conexion,dir = socket_server.accept()
                if aceptando == False:
                    conexion.send("Server Lleno".encode)
                    conexion.close()
                else:
                    if len(jugadoresOnline) == 0:
                        self.esperandoJugadores = int(conexion.recv(2048).decode())
                    jugadoresOnline.append(conexion)
                    if len(jugadoresOnline)==self.esperandoJugadores:
                        print("ya no se aceptan mas jugadores")
                        aceptando = False
                    hilo = Hilo_Partida(conexion,dir,self)
                    hilo.start()
                    hilos.append(hilo)
            except Exception as e:
                print(e)
server = Servidor()
server.iniciar()