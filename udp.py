from socket import *
import threading

class UdpClient():
    def __init__(
            self,        
            ip = "127.0.0.1",
            port = 11111,
            buffer_size: int = 32768
            ):
        self.src_addr = (ip, port)
        self.buffer_size = buffer_size

        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(self.src_addr)

        self.running = False
        self.thread = None

    def send(
            self, 
            data: bytes,
            ip = "127.0.0.1",
            port = 22222,
            ):
        self.sock.sendto(data, (ip, port))

    def receive(self) -> bytes:
        return self.sock.recv(self.buffer_size)
    
    def start(self, callback):
        self.running = True

        self.thread = threading.Thread(
            target=self._receive_loop,
            args=(callback,),
            daemon=True,
        )
        self.thread.start()

    def _receive_loop(self, callback):
        while self.running:
            try:
                callback(self.receive())
            except OSError:
                break

    def stop(self):
        self.running = False
        self.sock.close()