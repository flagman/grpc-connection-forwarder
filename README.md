# gRPC Connection Forwarder

`grpc_connection_forwarder` is a Python package that helps you forward incoming TCP connections to a gRPC server. It is particularly useful when you need to track the number of active connections.

## Features

- Forward incoming TCP connections to a gRPC server
- Connection counter with callback support
- Thread-safe implementation
- Easy integration with existing gRPC servers

## Installation

You can install `grpc_connection_forwarder` using pip:

```bash
pip install grpc_connection_forwarder
```

## Usage 

Here's a simple example of how to use grpc_connection_forwarder with a gRPC server:

```python 
import grpc
from grpc_connection_forwarder import GrpcConnnectionForwarder
from your_grpc_package import YourGRPCServer

# Initialize your gRPC server
grpc_server = grpc.server(thread_pool=ThreadPoolExecutor())
your_grpc_service = YourGRPCServer()
# ... (add your services to the gRPC server)

# Define a callback function to handle connection count changes (optional)
def connection_count_callback(count):
    print(f"Connected users: {count}")

# Initialize the gRPC Connection Forwarder
forwarder = GrpcConnnectionForwarder(grpc_server, callback=connection_count_callback)

# Start the forwarder
forwarder.serve(host='localhost', port=50051)
``` 

## Contributing
We welcome contributions to `grpc_connection_forwarder`. If you find a bug or want to propose a new feature, please open a GitHub issue or submit a pull request.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
