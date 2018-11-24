import struct
import select
import socket


def read_ready(sock, timeout, debug):
    sock = [sock] if isinstance(sock, list) is False else sock
    read, _, err = select.select(sock, [], sock, timeout)
    if len(err) != 0: return 2
    if len(read) == 0: return 1
    return 0


class Sockets:
    @staticmethod
    def connect(host, port, timeout=10, debug=False):
        sock = socket.socket()
        sock.settimeout(timeout)
        try:
            port = int(port)
            sock.connect((host, port))
            sock.settimeout(60)
            return sock
        except Exception as e:
            if debug: print "[ERROR] Sockets.connect: " + str(e)
            return False

    @staticmethod
    def send(sock, data, debug=False):
        try:
            data = "{0}{1}".format(struct.pack('>I', len(data)), data)
            length = len(data)
            sent = 0

            while sent < length: sent += sock.send(data)

            return True
        except Exception as e:
            if debug: print "[ERROR] Sockets.send: " + str(e)
            return False

    @staticmethod
    def recv(sock, timeout=60, buff_size=4096, debug=False):
        try:
            data = ''

            while len(data) < 4:
                if select.select([sock], [], [], timeout)[0] == []: return 1
                data += sock.recv(buff_size)

            length = struct.unpack('>I', data[:4])[0]
            data = data[4:]

            while len(data) < length:
                if select.select([sock], [], [], timeout)[0] == []: return 1
                data += sock.recv(buff_size)

            return data
        except Exception as e:
            if debug: print "[ERROR] Sockets.recv: " + str(e)
            return 2

    @staticmethod
    def close(sock):
        try: sock.shutdown(socket.SHUT_RDWR)
        except: pass
        finally:
            try: sock.close()
            except: pass


class Clearnet:
    @staticmethod
    def recv(conn, timeout=60, debug=False):
        try:
            data = ''

            while True:
                if read_ready(conn, timeout, debug) != 0: return False
                buff = conn.recv(16384)
                data += buff
                if len(buff) < 16384 and read_ready(conn, 0.5, debug) == 1: break

            return (data if data != '' else False)
        except Exception as e:
            if debug: print "[ERROR] (Clearnet.recv) could not receive data, reason: " + str(e)
            return False

    @staticmethod
    def bare_recv(conn, timeout=60, buff_size=8192, debug=False):
        try: return conn.recv(buff_size)
        except Exception as e:
            if debug: print "[ERROR] (Clearnet.bare_recv) could not receive data, reason: " + str(e)
            return False

    @staticmethod
    def send(conn, data, debug=False):
        try:
            sent = 0
            data_len = len(data)
            while sent < data_len: sent = conn.send(data[sent:])
            return True
        except Exception as e:
            if debug: print "[ERROR] (Clearnet.send) could not send data, reason: " + str(e)
            return False

    @staticmethod
    def bare_send(conn, data, debug=False):
        try: conn.sendall(data)
        except Exception as e:
            if debug: print "[ERROR] (Clearnet.bare_send) could not send data, reason: " + str(e)
            return False
