# ServerFrame

> Python base class for easily creating socket servers.

## USAGE

### Hello World Server

```python
from sockets import Sockets
from threadedserver import ThreadedServer

class Server(ThreadedServer):
    def __init__(self, port):
        ThreadedServer.__init__(self, port, debug=True)
    
    def on_connect(self, conn_info):
        conn, addr = conn_info
        Sockets.send(conn, "Hello world!")
        Sockets.close(conn)
```

### Echo Server

```python
from sockets import Sockets
from threadedserver import ThreadedServer

class Server(ThreadedServer):
    def __init__(self, port):
        ThreadedServer.__init__(self, port, debug=True)
    
    def on_connect(self, conn_info):
        conn, addr = conn_info
        data = Sockets.recv(conn)

        if data not in [1, 2]: Sockets.send(conn, data)
        Sockets.close(conn)
```
