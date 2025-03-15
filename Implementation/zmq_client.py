import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:2000")

for request in range(10):
    print(f"Sending request {request}...")
    socket.send(b"Hello")
    message = socket.recv()
    print(f"Received reply {request}: {message}")