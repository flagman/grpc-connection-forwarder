import socket
import threading
from connection_counter import ConnectionCounter
from lock_with_value import LockWithValue
import logging


class GrpcConnnectionForwarder:
    def __init__(self, grpc_server, callback=None):
        self.grpc_server = grpc_server
        self.connection_counter = ConnectionCounter(callback)

    def serve(self, host='localhost', port=50051):
        self._start_grpc_server()
        self._start_tcp_server(host, port)

    def _start_grpc_server(self):
        self.grpc_port = self.grpc_server.add_insecure_port('localhost:0')
        self.grpc_server.start()

    def _start_tcp_server(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server:
            tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcp_server.bind((host, port))
            tcp_server.listen(1)

            logging.info(f"Forwarder is running on port {port}")

            try:
                while True:
                    client_socket, _ = tcp_server.accept()
                    self._handle_connection(client_socket)
            except Exception as e:
                logging.exception("Exception occurred:", e)
            finally:
                self.grpc_server.stop(None)
                self.grpc_server.wait_for_termination()

    def _handle_connection(self, client_socket):
        self.connection_counter.increment()
        grpc_socket = socket.create_connection(('localhost', self.grpc_port))
        decremented_flag = LockWithValue()
        threading.Thread(target=self._forward, args=(
            client_socket, grpc_socket, decremented_flag)).start()
        threading.Thread(target=self._forward, args=(
            grpc_socket, client_socket, decremented_flag)).start()

    def _forward(self, src, dst, decremented_flag):
        try:
            self._transfer_data(src, dst)
        except OSError as e:
            if e.errno != 9:  # Bad file descriptor
                logging.exception("OSError occurred during forwarding:", e)
        except Exception as e:
            logging.exception("Error occurred during forwarding:", e)
        finally:
            self._close_sockets(src, dst, decremented_flag)

    def _transfer_data(self, src, dst):
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)

    def _close_sockets(self, src, dst, decremented_flag):
        src.close()
        dst.close()

        with decremented_flag.lock:
            if not decremented_flag.value:
                self.connection_counter.decrement()
                decremented_flag.value = True
