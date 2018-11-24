import select
import socket
import Sockets
import threading
from time import sleep


class ThreadedServer:
    def __init__(self, port, debug=False):
        self.running = False
        self.__debug = debug
        self.__port = port

    def start(self):
        if self.running: return

        t = threading.Thread(target=self.__listen)
        t.setDaemon(True)
        t.start()

    def stop(self):
        if self.running is False: return

        if self.__debug: print "[INFO] ThreadedServer stopped"
        self.running = False
        sleep(1)
        Sockets.close(self.__sock)

    def __listen(self):
        self.running = True

        self.__sock = socket.socket()
        self.__sock.bind(('0.0.0.0', self.__port))
        self.__sock.listen(5)

        if self.__debug: print "[INFO] ThreadedServer started"

        while self.running:
            try:
                if select.select([self.__sock], [], [], 0.5)[0] != []:
                    t = threading.Thread(target=self.on_connect, args=(self.__sock.accept(),))
                    t.setDaemon(True)
                    t.start()
            except socket.error as e:
                if self.__debug: print "[SOCKET ERROR] ThreadedServer.__listen: " + str(e)
            except Exception as e:
                if self.__debug: print "[ERROR] ThreadedServer.__listen: " + str(e)

    def __del__(self):
        self.stop()
